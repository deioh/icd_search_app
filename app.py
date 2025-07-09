import os
import socket
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect, FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='templates/web_app/templates')
app.logger.info('Flask application starting up...')
app.secret_key = os.urandom(24)
csrf = CSRFProtect(app)

# Configure Flask's logger to write to a file
file_handler = logging.FileHandler(os.path.join(app.root_path, 'logs', 'app.log'))
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

# Configure a specific logger for edit actions
edit_log_handler = logging.FileHandler(os.path.join(app.root_path, 'logs', 'icd_edit_log.txt'))
edit_log_handler.setLevel(logging.INFO)
edit_formatter = logging.Formatter('%(asctime)s - %(message)s')
edit_log_handler.setFormatter(edit_formatter)
edit_logger = logging.getLogger('icd_edit')
edit_logger.addHandler(edit_log_handler)
edit_logger.setLevel(logging.INFO)


import json

with open(os.path.join(app.root_path, 'config', 'settings.json')) as config_file:
    config_data = json.load(config_file)
    app.config.update(config_data)

# Explicitly set SQLALCHEMY_DATABASE_URI to an absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'icdcodes.db')}"


db = SQLAlchemy(app)

# Define the User model for authentication
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Define the login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Command to create a default admin user
@app.cli.command("create-admin")
def create_admin():
    """Creates a default admin user."""
    with app.app_context():
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin = User(username='admin')
            admin.set_password('admin')  # Change this in a production environment!
            db.session.add(admin)
            db.session.commit()
            print("Admin user created.")
        else:
            print("Admin user already exists.")

# Define the ICDCode ORM model
class ICDCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<ICDCode {self.code}>'

# Define the form for adding/editing ICD codes
class ICDCodeForm(FlaskForm):
    code = StringField('ICD Code', validators=[DataRequired(), Length(max=20)])
    description = StringField('Description', validators=[DataRequired(), Length(max=500)])
    category = StringField('Category (Optional)', validators=[Length(max=100)])
    submit = SubmitField('Submit')

# Create database tables if they don't exist
with app.app_context():
    db.create_all()
    print("Database tables created/checked.")

# Basic search endpoint
@app.route('/search')
def search():
    query = request.args.get('q', '')
    with open('search_debug.log', 'a') as f:
        f.write(f"Search query received: '{query}'\n")
    if query:
        # Search for codes or descriptions matching the query
        results = ICDCode.query.filter(
            (ICDCode.code.ilike(f'%{query}%')) |
            (ICDCode.description.ilike(f'%{query}%'))
        )
        with open('search_debug.log', 'a') as f:
            f.write(f"SQL Query: {results}\n")
        results = results.all()
        with open('search_debug.log', 'a') as f:
            f.write(f"Number of results found: {len(results)}\n")
    else:
        results = []
    return render_template('index.html', query=query, results=results)

@app.route('/')
def index():
    app.logger.info('Index route accessed.')
    return render_template('index.html', query='', results=[])

@app.route('/get_one_icd')
def get_one_icd():
    icd_entry = ICDCode.query.first()
    print(f"Attempting to retrieve ICD entry. Result: {icd_entry}")
    if icd_entry:
        return f"Found ICD Entry: Code - {icd_entry.code}, Description - {icd_entry.description}"
    else:
        return "No ICD entries found in the database."

# Management Interface Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['user_logged_in'] = True
            session['username'] = user.username
            flash('You have been logged in!', 'success')
            return redirect(url_for('manage_icd_codes'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_logged_in', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/manage')
def manage_icd_codes():
    form = ICDCodeForm()
    if not session.get('user_logged_in'):
        return redirect(url_for('login'))
        
    query = request.args.get('query', '')
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of entries per page

    if query:
        # Search for codes or descriptions matching the query
        results = ICDCode.query.filter(
            (ICDCode.code.ilike(f'%{query}%')) |
            (ICDCode.description.ilike(f'%{query}%'))
        ).paginate(page=page, per_page=per_page, error_out=False)
    else:
        results = ICDCode.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('manage.html', 
                           entries=results.items, 
                           pagination=results, 
                           query=query,
                           user_logged_in=session.get('user_logged_in'),
                           username=session.get('username'),
                           form=form)

@app.route('/manage/add', methods=['POST'])
def add_icd_code():
    form = ICDCodeForm()
    if form.validate_on_submit():
        code = form.code.data
        description = form.description.data
        category = form.category.data

        try:
            new_code = ICDCode(code=code, description=description, category=category)
            db.session.add(new_code)
            db.session.commit()
            flash('ICD Code added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding ICD Code: {e}', 'error')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'error')
    return redirect(url_for('manage_icd_codes'))

@app.route('/manage/edit/<int:id>', methods=['POST'])
def edit_icd_code(id):
    icd_entry = ICDCode.query.get_or_404(id)
    form = ICDCodeForm()
    username = session.get('username', 'anonymous')

    if form.validate_on_submit():
        try:
            icd_entry.code = form.code.data
            icd_entry.description = form.description.data
            icd_entry.category = form.category.data
            db.session.commit()
            flash('ICD Code updated successfully!', 'success')
            edit_logger.info(f"action: edit, code: {icd_entry.code}, user: {username}, result: success")
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating ICD Code: {e}', 'error')
            edit_logger.error(f"action: edit, code: {icd_entry.code}, user: {username}, result: failure, reason: {e}")
    else:
        errors = '; '.join([f'{field}: {", ".join(error_list)}' for field, error_list in form.errors.items()])
        edit_logger.warning(f"action: edit, code: {icd_entry.code}, user: {username}, result: failure, reason: Validation failed - {errors}")
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", "error")

    return redirect(url_for('manage_icd_codes'))

@app.route('/manage/delete/<int:id>', methods=['POST'])
def delete_icd_code(id):
    icd_entry = ICDCode.query.get_or_404(id)
    try:
        db.session.delete(icd_entry)
        db.session.commit()
        flash('ICD Code deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting ICD Code: {e}', 'error')
    return redirect(url_for('manage_icd_codes'))



if __name__ == '__main__':
    # Get dynamic LAN IP
    hostname = socket.gethostname()
    try:
        lan_ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        lan_ip = "127.0.0.1" # Fallback to localhost if unable to get LAN IP

    print(f"* Running on http://{lan_ip}:5000/")
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
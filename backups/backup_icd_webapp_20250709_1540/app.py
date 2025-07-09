import os
import socket
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates/web_app/templates')

# Configure Flask's logger to write to a file
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

import json

with open(os.path.join(app.root_path, 'config', 'settings.json')) as config_file:
    config_data = json.load(config_file)
    app.config.update(config_data)

# Explicitly set SQLALCHEMY_DATABASE_URI to an absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'icdcodes.db')}"


db = SQLAlchemy(app)

# Define the ICDCode ORM model
class ICDCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<ICDCode {self.code}>'

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
@app.route('/manage')
def manage_icd_codes():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of entries per page
    entries = ICDCode.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('manage.html', entries=entries.items, pagination=entries, flashed_messages=get_flashed_messages())

@app.route('/manage/add', methods=['POST'])
def add_icd_code():
    code = request.form['code']
    description = request.form['description']
    category = request.form.get('category')

    if not code or not description:
        flash('ICD Code and Description are required!', 'error')
        return redirect(url_for('manage_icd_codes'))

    try:
        new_code = ICDCode(code=code, description=description, category=category)
        db.session.add(new_code)
        db.session.commit()
        flash('ICD Code added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding ICD Code: {e}', 'error')
    return redirect(url_for('manage_icd_codes'))

@app.route('/manage/edit/<int:id>', methods=['POST'])
def edit_icd_code(id):
    icd_entry = ICDCode.query.get_or_404(id)
    icd_entry.code = request.form['code']
    icd_entry.description = request.form['description']
    icd_entry.category = request.form.get('category')

    try:
        db.session.commit()
        flash('ICD Code updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating ICD Code: {e}', 'error')
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

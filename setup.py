from setuptools import setup, find_packages

setup(
    name='icd_search_app',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
    ],
    entry_points={
        'console_scripts': [
            'icd_search_app = icd_search_app.cli:main',
        ],
    },
)

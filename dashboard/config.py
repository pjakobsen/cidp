import os
# This simply points to the local directory
basedir = os.path.abspath(os.path.dirname(__file__))

print basedir

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/cidp'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
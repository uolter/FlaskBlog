import os

CSRF_ENABLED = True
SECRET_KEY = 'Chamber of Secrets :D'
try:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
except KeyError:
    print 'DATABASE_URL not set'

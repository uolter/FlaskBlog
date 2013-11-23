from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ajay:12345@localhost/man'

db = SQLAlchemy()
db.app = app
db.init_app(app)
migrate = Migrate(app, db)
manager = Manager(app)

from app import models
from app import views

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import *
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
fim = 3
engine = create_engine('postgres://localhost/crs')
engine.echo = True
conn = engine.connect()

from app import views, models

    

from flask import Flask
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime


# initialize first flask
app = Flask(__name__)
app.secret_key = 'futbolas'

# Set Databse patch and data
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mrka_esu:Labasrytas12345@93.127.213.123:3306/mrka_eshop'

class Base(DeclarativeBase):
    createdBy = Column(String(50), nullable=False, default='System')
    modifiedBy = Column(String(50), nullable=False, default='System')
    createdDate = Column(DateTime, default=datetime.datetime.now)
    modifiedDate = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    deleted = Column(Boolean, default=False)

db = SQLAlchemy(app, model_class=Base)
migrate = Migrate(app, db)


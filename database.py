import datetime
from sqlalchemy.orm import DeclarativeBase
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Column,String, DateTime, Boolean

 
# initialize first flask
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///parduotuve.db'
app.config['SECRET_KEY'] = 'Slapta_labai_labai'

 
class Base(DeclarativeBase):
    createdBy = Column(String(50), nullable=False, default='System')
    modifiedBy = Column(String(50), nullable=False, default='System')
    createdDate = Column(DateTime, default=datetime.datetime.now)
    modifiedDate = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    deleted = Column(Boolean, default=False)
 
db = SQLAlchemy(app, model_class=Base)
migrate = Migrate(app, db)
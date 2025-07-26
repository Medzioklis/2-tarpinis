from flask import Flask
from flask_login import LoginManager
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime


# initialize first flask
app = Flask(__name__)
app.secret_key = 'futbolas'

# Set Databse patch and data
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ugne:Labasrytas2025!@35.242.231.50:3306/futbolas' #'mysql+pymysql://mrka_esu:Labasrytas12345@93.127.213.123:3306/mrka_eshop'

class Base(DeclarativeBase):
    createdBy = Column(String(50), nullable=False, default='System')
    modifiedBy = Column(String(50), nullable=False, default='System')
    createdDate = Column(DateTime, default=datetime.datetime.now)
    modifiedDate = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    deleted = Column(Boolean, default=False)

login_manager = LoginManager(app) # Tai sukuria LoginManager objektą ir pririša jį prie Flask aplikacijos. Šis objektas atsakingas už prisijungimo valdymą, naudotojo sesijos atkūrimą, nukreipimą į prisijungimo puslapį, jei naudotojas neprisijungęs.
login_manager.init_app(app)       # šita eilutė inicijuoja LoginManager su Flask aplikacija
login_manager.login_view = 'login' # nurodo kurį route naudoti, kai neprisijungęs naudotojas bando pasiekti saugomą puslapį.

db = SQLAlchemy(app, model_class=Base)
migrate = Migrate(app, db)


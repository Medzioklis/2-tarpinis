from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from flask_admin import Admin
from flask_migrate import Migrate
import datetime

# Aplikacijos konfiguracija
app = Flask(__name__)
app.config['SECRET_KEY'] = 'futbolas'  # Slaptas raktas sesijoms

# Duomenų bazės kelias
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://marius:Labasrytas2025!@35.242.231.50:3306/futbolas'

# cia ikeliam base kad visom lentelems kurtu
class Base(DeclarativeBase):
    createdBy = Column(String(50), nullable=False, default='System')
    modifiedBy = Column(String(50), nullable=False, default='System')
    createdDate = Column(DateTime, default=datetime.datetime.now)
    modifiedDate = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    deleted = Column(Boolean, default=False)

# Startuojame (Inicializuojame) pletinius (Extensionus)
# Flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # nurodo kurį route naudoti, kai neprisijungęs naudotojas bando pasiekti saugomą puslapį.
# Pranešimo kategorija ir tekstas
login_manager.login_message = "Prašome prisijungti, kad pasiektumėte šį puslapį."
login_manager.login_message_category = "info"

# Inicializuojame Admin sąsają
admin = Admin(app, name='Vartotojų Valdymas', template_mode='bootstrap4')

# SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)


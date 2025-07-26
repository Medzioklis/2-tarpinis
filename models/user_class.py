from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(25), nullable=False)
    user_lastname = db.Column(db.String(25), nullable=False)
    user_email = db.Column(db.String(50), nullable=False, unique=True)
    user_password = db.Column(db.String(255), nullable=False)
    user_role = db.Column(db.Integer, default=2)
    is_admin = db.Column(db.Boolean, default=False) # --- PRIDĖTA Flask-admin ---


    login_security = db.relationship('LoginSecurity', uselist=False, back_populates='user', cascade="all, delete-orphan")

    def set_password(self, password):
        self.user_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.user_password, password)


    def __str__(self):
        return f'Vartotojas: {self.user_name} {self.user_lastname}, paštas: {self.user_email}, slaptažodis: {self.user_password}'
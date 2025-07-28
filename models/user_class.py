from database import db, login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(25), nullable=False)
    user_lastname = db.Column(db.String(25), nullable=False)
    user_email = db.Column(db.String(50), nullable=False, unique=True)
    user_password = db.Column(db.String(255), nullable=False)
    user_role = db.Column(db.Integer, default=2)

    # rysys su Loginsecurity 
    login_security = db.relationship('LoginSecurity', uselist=False, back_populates='user', cascade="all, delete-orphan")

    def __str__(self):
        return f'Vartotojas: {self.user_name} {self.user_lastname}, paštas: {self.user_email}, slaptažodis: {self.user_password}'
    
class LoginSecurity(db.Model):
    __tablename__ = 'login_security'
    id = db.Column(db.Integer, primary_key=True)
    login_attempts = db.Column(db.Integer, default=0)
    blocked_until = db.Column(db.DateTime, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', back_populates='login_security')

# Flask-Login reikalauja šios funkcijos, kad gautų vartotoją pagal jo ID
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
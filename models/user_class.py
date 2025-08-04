from database import db
from werkzeug.security import check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String(25), nullable=False)
    user_lastname = db.Column(db.String(25), nullable=False)
    user_email = db.Column(db.String(50), nullable=False, unique=True)
    user_password = db.Column(db.String(255), nullable=False)
    user_role = db.Column(db.Integer, default=2)
    user_balance = db.Column(db.Float, default=0.0)
    
    # Vartotojas turi daug krepšelio prekių (Cart įrašų)
    cart_items = db.relationship('Cart', back_populates='user')

    login_security = db.relationship('LoginSecurity', uselist=False, back_populates='user')
    reviews = db.relationship("Review", back_populates="user", lazy='dynamic')


    # backref yra SQLAlchemy magija kuria jis pats atmintyje sukuria Order modelyje customer, skiriasi nuo back_populates tuo kad nebutina kode apsirasyt customer
    orders = db.relationship('Order', backref='user', lazy='dynamic')


    def check_password(self, password):
        return check_password_hash(self.user_password, password)


    def __str__(self):
        return f'Vartotojas: {self.user_name} {self.user_lastname}, paštas: {self.user_email}, slaptažodis: {self.user_password}'
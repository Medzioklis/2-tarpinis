from database import db

class LoginSecurity(db.Model):
    __tablename__ = 'login_security'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    login_attempts = db.Column(db.Integer, default=0)
    blocked_until = db.Column(db.DateTime, nullable=True)

    user = db.relationship('User', back_populates='login_security')
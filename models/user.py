from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key= True, autoincrement= True)
    user_name = db.Column(db.String(50), nullable=False)
    user_lastname = db.Column(db.String(50), nullable=False)
    user_email = db.Column(db.String(255), nullable=False, unique=True)
    user_password = db.Column(db.String(100), nullable=False)
    user_perm = db.Column(db.Integer, default=2, nullable=False)

    def set_password(self, password):
        self.user_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.user_password, password)
        
    def __repr__(self):
        return f"<User {self.id}: {self.user_name} {self.user_lastname}, {self.user_email}>"


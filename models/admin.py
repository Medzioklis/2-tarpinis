from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from flask_admin import AdminIndexView
from flask import redirect, url_for



class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100), nullable=False)
    admin_perm = db.Column(db.Integer, default=1, nullable=False)

    def set_password(self, password):
        self.slaptazodis = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.slaptazodis, password)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"<Admin {self.id}: {self.admin_name}>"
    
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
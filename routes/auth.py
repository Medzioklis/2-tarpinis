from flask import Blueprint, redirect, url_for, flash
from services.auth_functions import user_login, add_user
from flask_login import logout_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return user_login()

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    return add_user()

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash("Sėkmingai atsijungėte.", "success")
    return redirect(url_for('home.index'))  
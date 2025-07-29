from flask import Blueprint
from services.user_functions import user_login, add_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return user_login()

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    return add_user()
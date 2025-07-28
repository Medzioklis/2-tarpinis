from flask import Blueprint
from services.user_functions import user_login

login_bp = Blueprint('login', __name__, url_prefix='/login', template_folder='../templates')

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    return user_login()
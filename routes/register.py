from flask import Blueprint
from services.user_functions import add_user

register_bp = Blueprint('register', __name__, url_prefix='/register', template_folder='../templates')

@register_bp.route('/add_user', methods=['GET', 'POST'])
def register():
    return add_user()
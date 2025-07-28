from flask import Blueprint, render_template
from flask_login import login_required, current_user

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard', template_folder='../templates')

@dashboard_bp.route('/')
@login_required
def dashboard():
    if current_user.user_role == 1:
        return render_template('admin_dashboard.html')
    else:
        return render_template('user_dashboard.html')
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user


user_bp = Blueprint('user', __name__, url_prefix='/user', template_folder='../templates')


@user_bp.route('/')
@login_required
def user_dashboard():
    if current_user.user_role != 2:
        flash("Neturite prieigos prie naudotojo puslapio.", "danger")
        return redirect(url_for('login'))
    return render_template('user_dashboard.html', user=current_user)
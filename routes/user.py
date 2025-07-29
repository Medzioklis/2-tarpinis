from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from services.user_functions import top_up_balance


user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/')
@login_required
def dashboard():
    if current_user.user_role != 2:
        flash("Neturite prieigos prie naudotojo puslapio.", "danger")
        return redirect(url_for('auth.login'))
    return render_template('user/dashboard.html', user=current_user)


@user_bp.route('/add_balance', methods = ['GET','POST'])
@login_required
def add_balance():
    return top_up_balance()



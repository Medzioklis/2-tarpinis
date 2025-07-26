from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from services.user_functions import add_view_admin


admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='../templates')


@admin_bp.route('/')
@login_required
def admin_dashboard():
    if current_user.user_role != 1:
        flash("Neturite prieigos prie administratoriaus puslapio.", "danger")
        return redirect(url_for('login'))
    admin_view = add_view_admin()
    return render_template('admin_dashboard.html', user=current_user, view = admin_view)

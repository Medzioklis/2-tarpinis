from flask import Blueprint, redirect, url_for
from flask import flash
from flask_login import logout_user, login_required

logout_bp = Blueprint('logout', __name__, url_prefix='/logout', template_folder='../templates')

@logout_bp.route('/')
@login_required
def logout():
    logout_user()
    flash('Sėkmingai atsijungėte.', 'info')
    return redirect(url_for('home.home'))
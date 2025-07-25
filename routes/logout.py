from flask import Blueprint, flash, redirect
from flask_login import login_required, logout_user

logout_bp = Blueprint('logout', __name__, url_prefix='/logout', template_folder='../templates')

@logout_bp.route('/')
@login_required
def logout():
    logout_user()
    flash("Sėkmingai atsijungėte.", "success")
    return redirect('/login')

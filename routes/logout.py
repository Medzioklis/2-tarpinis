from flask import Blueprint, flash, redirect, url_for
from flask_login import logout_user, login_required

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/')
@login_required
def logout():
    logout_user()
    flash("Sėkmingai atsijungėte.", "success")
    return redirect(url_for('home.index'))  # Nukreipia į pagrindinį puslapį po atsijungimo

from database import db, app
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager,login_user, logout_user, login_required, current_user
from sqlalchemy import select, func
from flask_admin.contrib.sqla import ModelView
from models.user import User
from models.admin import Admin


class ProtectedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Automatiškai nukreipti pagal rolę
        if isinstance(current_user, Admin):
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('user_dashboard'))
        
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        stmt = select(Admin).where(Admin.admin_name == username)
        admin = db.session.execute(stmt).scalar_one_or_none()

        if admin and admin.check_password(password):
            login_user(admin)
            return redirect(url_for('admin_dashboard')) # dar nesukurtas html, tai kolkas palieku šitaip

        stmt = select(User).where(User.user_email == username)
        user = db.session.execute(stmt).scalar_one_or_none()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('user_dashboard')) # dar nesukurtas html, tai kolkas palieku šitaip

        flash("Neteisingi prisijungimo duomenys.", "danger")

    return render_template('login.html')

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if not isinstance(current_user, Admin):
        flash("Neturite prieigos prie administratoriaus puslapio.", "danger")
        return redirect(url_for('login'))
    return "Sveiki, administratoriau!"

@app.route('/user_dashboard')
@login_required
def user_dashboard():
    if not isinstance(current_user, User):
        flash("Neturite prieigos prie naudotojo puslapio.", "danger")
        return redirect(url_for('login'))
    return "Sveiki, vartotojau!"


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Sėkmingai atsijungėte.", "success")
    return redirect('/login')





from database import db, app
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import select, func
from flask_admin.contrib.sqla import ModelView
from models.user import User
from forms.login_form import LoginForm
from datetime import datetime, timedelta


class ProtectedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role==1
    
    def inaccessible_callback(self, name, **kwargs):
        flash("Neturite prieigos.", "danger")
        return redirect(url_for('login'))

    
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form= LoginForm()

    if current_user.is_authenticated:
        # Automatiškai nukreipti pagal rolę
        if current_user.user_role ==1:
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('user_dashboard'))

    if form.validate_on_submit():
        stmt = select(User).where(User.user_email == form.email.data)
        user = db.session.execute(stmt).scalar_one_or_none()

        now = datetime.now()
        if user:
            if user.blocked_until and user.blocked_until > now:
                time_left = int((user.blocked_until - now).total_seconds() // 60)
                flash(f"Per daug neteisingų bandymų. Bandykite po {time_left} min.", "danger")
                return render_template('login.html', form=form)

            if user and user.check_password(form.password.data):
                user.login_attempts = 0
                user.blocked_until = None
                db.session.commit()
                login_user(user)
                return redirect(url_for('admin_dashboard') if user.user_role == 1 else url_for('user_dashboard'))
            else:
                user.login_attempts = (user.login_attempts or 0) + 1
                if user.login_attempts >= 3:
                    user.blocked_until = now + timedelta(minutes=2)
                    flash("Per daug neteisingų bandymų. Pabandykite po 2 minučių.", "danger")
                    return redirect(url_for('user_dashboard'))
                else:
                    flash("Neteisingi prisijungimo duomenys.", "danger")
                db.session.commit()
        else:
            flash("Vartotojas nerastas.", "danger")
            return render_template("login.html", form=form)

    return render_template('login.html', form=form)


@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.user_role != 1:
        flash("Neturite prieigos prie administratoriaus puslapio.", "danger")
        return redirect(url_for('login'))
    return render_template("admin_dashboard.html")


@app.route('/user_dashboard')
@login_required
def user_dashboard():
    if current_user.user_role != 2:
        flash("Neturite prieigos prie naudotojo puslapio.", "danger")
        return redirect(url_for('login'))
    return "Sveiki prisijungę, turite vartotojo teises"


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Sėkmingai atsijungėte.", "success")
    return redirect('/login')





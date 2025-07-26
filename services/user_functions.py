from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash
from sqlalchemy import select
from database import db, login_manager
from datetime import datetime, timedelta
from models.user_class import User
from models.login_security_class import LoginSecurity
from forms.register_form import RegisterForm
from forms.login_form import LoginForm
from forms.balance_form import BalanceForm
from decimal import Decimal

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def add_user():
    form = RegisterForm()
    if form.validate_on_submit():
        stmt = db.select(User).where(User.user_email == form.email.data)
        form_email = db.session.execute(stmt).scalar_one_or_none()
        if form_email is None:
            name = form.name.data
            lastname = form.lastname.data
            email = form.email.data
            password1 = form.password1.data
            password2 = form.password2.data
            if password1 == password2:
                password = generate_password_hash(password1, method='pbkdf2:sha256')
            else:
                flash("Slaptažodžiai nesutampa!", 'alert')
                return render_template('add_user.html', form=form)
            new_user = User(user_name=name, user_lastname=lastname, user_email=email, user_password=password)
            db.session.add(new_user)
            db.session.commit()
            return render_template('registered_sucess.html', user=new_user)
        else:
            flash("Vartotojas su tokiu el. paštu jau egzistuoja.", 'alert')
            return render_template('add_user.html', form=form)
    return render_template('add_user.html', form=form)

def user_login():
    form= LoginForm()
    if current_user.is_authenticated:
        # Automatiškai nukreipti pagal rolę
        if current_user.user_role ==1:
            return redirect(url_for('admin.admin_dashboard'))
        else:
            return redirect(url_for('user.user_dashboard'))

    if form.validate_on_submit():
        stmt = select(User).where(User.user_email == form.email.data)
        user = db.session.execute(stmt).scalar_one_or_none()

        now = datetime.now()
        if user:
            login_security = user.login_security

            if login_security and login_security.blocked_until and login_security.blocked_until > now:
                time_left = int((login_security.blocked_until - now).total_seconds() // 60)
                flash(f"Per daug neteisingų bandymų. Bandykite po {time_left} min.", "danger")
                return render_template('login.html', form=form)

            if user.check_password(form.password.data):
                if not login_security:
                    login_security = LoginSecurity(user=user)  # Sukuria naują įrašą, jei nėra
                    db.session.add(login_security)

                login_security.login_attempts = 0
                login_security.blocked_until = None
                db.session.commit()
                login_user(user)
                return redirect(url_for('admin.admin_dashboard') if user.user_role == 1 else url_for('user.user_dashboard'))

            else:
                if not login_security:
                    login_security = LoginSecurity(user=user)
                    db.session.add(login_security)

                login_security.login_attempts = (login_security.login_attempts or 0) + 1

                if login_security.login_attempts >= 3:
                    login_security.blocked_until = now + timedelta(minutes=2)
                    flash("Per daug neteisingų bandymų. Pabandykite po 2 minučių.", "danger")
                    db.session.commit()
                    return redirect(url_for('login.login'))  # Ne redirect'as į dashboard, jei klaidinga

                else:
                    flash("Neteisingi prisijungimo duomenys.", "danger")
                db.session.commit()
        else:
            flash("Vartotojas nerastas.", "danger")
            return render_template("login.html", form=form)

    return render_template('login.html', form=form)


def top_up_balance():
    form = BalanceForm()
    if form.validate_on_submit():
        amount = float(form.amount.data)
        if current_user.user_balance is None:
            current_user.user_balance = 0.0
        current_user.user_balance += amount
        db.session.commit()
        flash(f"Sėkmingai papildyta {amount:.2f} €.", "success")
        return redirect(url_for('user.user_dashboard'))
    
    return render_template('balance_topup.html', form=form)

# amount = float(form.amount.data)  # vietoj Decimal
# if current_user.user_balance is None:
#     current_user.user_balance = 0.0
# current_user.user_balance += amount
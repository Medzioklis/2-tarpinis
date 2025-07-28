from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_user
from sqlalchemy import select
from forms.login_form import LoginForm
from models.user_class import User, LoginSecurity
from database import db
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta

login_bp = Blueprint('login', __name__, url_prefix='/login', template_folder='../templates')

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    # Jei vartotojas jau prisijungęs, nukreipiame jį į pagrindinį puslapį
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
        
    form = LoginForm()
    if form.validate_on_submit():
        # Pataisytas variantas
        user = db.session.scalars(db.select(User).where(User.user_email == form.email.data)).first()
        
        #========== Login-security =========================
        now = datetime.now()
        if user: # and user.deleted == False nuemiau patikrinima
            login_security = user.login_security

            if login_security and login_security.blocked_until and login_security.blocked_until > now:
                time_left = int((login_security.blocked_until - now).total_seconds() // 60) # formule kiek liko laiko iki unblock
                flash(f"Per daug neteisingų bandymų. Bandykite po {time_left} min.", "danger")
                return render_template('login.html', form=form)
            
            if check_password_hash(user.user_password, form.password.data): 
                if not login_security:
                    login_security = LoginSecurity(user=user)  # Sukuria naują įrašą, jei nėra
                    db.session.add(login_security)            

                login_security.login_attempts = 0
                login_security.blocked_until = None
                db.session.commit()
                login_user(user)
                if current_user.is_authenticated:
                    return redirect(url_for('dashboard.dashboard'))
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
                    flash(f"Neteisingas prisijungimas, bandymas {login_security.login_attempts}, 3 klaidos blokas 2 minutėms", "danger")
                db.session.commit()               
        else:
            flash("Vartotojas nerastas.", "danger")
            return render_template("login.html", form=form)
    return render_template('login.html', form=form) 

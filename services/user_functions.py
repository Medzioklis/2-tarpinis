from forms.balance_form import BalanceForm
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from models.user_class import db

# Sukuriama balanso papildymo forma pagal WTForms klasę `BalanceForm`
def top_up_balance():
    form = BalanceForm()
    if form.validate_on_submit():
        amount = float(form.amount.data)
        # Tikrina, jeigu naudotojo balansas neegzistuoja (None), priskiriama default reikšmė 0.0 €
        if current_user.user_balance is None:
            current_user.user_balance = 0.0
        # Pridedama papildymo suma prie esamo naudotojo balanso
        current_user.user_balance += amount
        db.session.commit()
        flash(f"Sėkmingai papildyta {amount:.2f} €.", "success")
        return redirect(url_for('user.dashboard'))
    
    return render_template('user/balance_topup.html', form=form)
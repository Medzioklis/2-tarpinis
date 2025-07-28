# Sukuriame apsaugotą ModelView, kad tik prisijungę vartotojai galėtų pasiekti admin panelę
from flask import flash, redirect, url_for, request
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

class SecureModelView(ModelView):
    def is_accessible(self):
        # Tikriname, ar vartotojas yra prisijungęs
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # Jei vartotojas neprisijungęs, nukreipiame į prisijungimo puslapį
        flash("Prašome prisijungti, kad pasiektumėte administravimo panelę.", "warning")
        return redirect(url_for('login.login', next=request.url))

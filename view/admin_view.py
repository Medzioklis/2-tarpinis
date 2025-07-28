from database import admin, db
from models.securemodel_class import SecureModelView
from models.user_class import User


# Pridedame User modelį į admin sąsają, naudodami mūsų apsaugotą view
# Čia galima konfigūruoti, kokie laukai matomi, redaguojami ir t.t.
admin.add_view(SecureModelView(User, db.session))

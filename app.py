from database import app
from routes.register import register_bp
from routes.home import home_bp
from routes.admin import admin_bp
from routes.user import user_bp
from routes.login import login_bp
from routes.logout import logout_bp


app.register_blueprint(home_bp)
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)
app.register_blueprint(logout_bp)

if __name__ == "__main__":
    app.run(debug=True)
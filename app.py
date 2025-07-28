from database import app
from routes.home_route import home_bp
from routes.login_route import login_bp
from routes.dashboard_route import dashboard_bp
from routes.logout_route import logout_bp
from routes.register_route import register_bp

app.register_blueprint(home_bp)
app.register_blueprint(login_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(register_bp)

if __name__ == "__main__":
    app.run(debug=True)


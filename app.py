from database import app
from routes.register import register_bp
from routes.home import home_bp
from routes.admin import admin_bp


app.register_blueprint(home_bp)
app.register_blueprint(register_bp)
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    app.run(debug=True)
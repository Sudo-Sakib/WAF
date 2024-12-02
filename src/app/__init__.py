from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Database and hashing utilities
db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    # Create a Flask application instance
    app = Flask(__name__, static_folder='../static')

    # Configure the app (you can add more configuration settings here later)
    app.config["SECRET_KEY"] = "your-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///waf.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)

    #CSRF
    app.config["SESSION_TYPE"] = 'filesystem' # store sessions on the filesystem

    #Initialize Flask Session
    Session(app)

    # Register Auth Route
    from app.routes.auth_routes import auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    # Register the Admin routes 
    from app.routes.admin.admin_routes import admin_blueprint
    app.register_blueprint(admin_blueprint)

    # Register Test Route
    from app.routes.test_routes import test_blueprint
    app.register_blueprint(test_blueprint)

    # Register File Route
    from app.routes.file_routes import file_blueprint
    app.register_blueprint(file_blueprint)

    # Register Admin Logs Route
    from app.routes.admin.admin_logs_routes import admin_log_blueprint
    app.register_blueprint(admin_log_blueprint)

    # Register Admin Custom Rule Route
    from app.routes.admin.custom_rule_routes import custom_rule_blueprint
    app.register_blueprint(custom_rule_blueprint)

    # Register Block IP Route
    from app.routes.block_ip_routes import ip_blueprint
    app.register_blueprint(ip_blueprint, url_prefix='/ip')
    
    # Register the User routes (URL endpoints)
    from app.routes.user.user_routes import user_blueprint
    app.register_blueprint(user_blueprint, url_prefix="/user")
    
    # Register User Logs Route
    from app.routes.user.user_logs_routes import user_log_blueprint
    app.register_blueprint(user_log_blueprint)


    return app

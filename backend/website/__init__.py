from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config["SECRET_KEY"] = "aashish_key"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'aashish_key'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True 
    app.config['MAIL_USERNAME'] = '201aashish@gmail.com'
    app.config['MAIL_PASSWORD'] = 'kzhcexwwskzmlqht'
    
    db.init_app(app)

    from . import models

    from .views import views
    from .auth import auth
    
    
    jwt = JWTManager(app)



    login_manager = LoginManager()
    login_manager.login_view = 'auth.api_admin_login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))
    
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        if user == None:
            return
        return user.id

    @jwt.additional_claims_loader
    def add_claims_to_access_token(user):
        if user == None:
            return{'role' : 'user'}
        return {'role': user.role.name}
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    with app.app_context():
        db.create_all()
        create_admin_user(db)
        
    return app

from .models import User, UserRole
def create_admin_user(db):
    admin_username = "201aashish@gmail.com"
    admin_password = "aashish" 

    admin = User.query.filter_by(email=admin_username).first()

    if not admin:
        admin = User(
            email=admin_username,
            password=generate_password_hash(admin_password, method='sha256'),
            first_name="Admin",
            role=UserRole.admin
        )
        db.session.add(admin)
        db.session.commit()

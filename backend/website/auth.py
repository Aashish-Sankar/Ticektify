from flask import Blueprint, jsonify, request
import flask_login
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import models
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta, date


auth = Blueprint('auth', __name__)


def generate_access_token(user):
    access_token = create_access_token(identity=user, expires_delta=timedelta(hours=1))
    return access_token


@auth.route('/api/user/login', methods=['POST'])
def api_user_login():
    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')

        user = models.User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                access_token = generate_access_token(user)
                response =  jsonify({
                    "message": "Logged in successfully!",
                    "user": {
                        "email": user.email,
                        "first_name": user.first_name,
                        "role": user.role.name
                    },
                    "access_token": access_token
                })
                response.headers['Access-Control-Allow-Origin'] = '*'
                last = models.LastLogin.query.filter_by(user_id=user.id).first()
                print(last)
                if last:
                    last.lastlogin = date.today()
                    db.session.add(last)
                    db.session.commit()
                else:
                    new_lastlogindate = models.LastLogin(lastlogin=date.today(), user_id=user.id)
                    db.session.add(new_lastlogindate)
                    db.session.commit()
                return response
            else:
                return jsonify({"error": "Incorrect password, try again"})
        else:
            return jsonify({"error": "Email does not exist"})

@auth.route('/api/admin/login', methods=['POST'])
def api_admin_login():
    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')

        user = models.User.query.filter_by(email=email).first()
        if user:
            if user.role == models.UserRole.admin:
                if check_password_hash(user.password, password):
                    access_token = generate_access_token(user)
                    response = jsonify({
                        "message": "Logged in successfully!",
                        "user": {
                    "id" : user.id,
                    "email" : user.email,
                    "firstName" : user.first_name,
                    "role" : user.role.name
                },
                        "access_token": access_token
                    })
                    response.headers['Access-Control-Allow-Origin'] = '*'
                    return response
                else:
                    return jsonify({"error": "Incorrect password, try again"})
            else:
                return jsonify({"error": "You are not an admin!"})
        else:
            return jsonify({"error": "Email does not exist"})

@auth.route('/api/user/signUp', methods=['POST'])
def api_user_signUp():
    if request.method == 'POST':
        email = request.json.get('email')
        first_name = request.json.get('firstName')
        password1 = request.json.get('password1')
        password2 = request.json.get('password2')
        role = request.json.get('role')

        user = models.User.query.filter_by(email=email).first()
        if user:
            return jsonify({"error": "Email already exists"})
        elif len(email) < 4:
            return jsonify({"error": "Email is too short"})
        elif len(first_name) < 2:
            return jsonify({"error": "First Name is too short"})
        elif len(password1) < 7:
            return jsonify({"error": "Password is too short"})
        elif password1 != password2:
            return jsonify({"error": "Password not matching"})
        else:
            hashed_password = generate_password_hash(password1, method='sha256')
            new_user = models.User(email=email, first_name=first_name, password=hashed_password, role='user')
            db.session.add(new_user)
            db.session.commit()
            access_token = generate_access_token(user)
            response = jsonify({
                "message": "Account Created!",
                "user": {
                    "id" : new_user.id,
                    "email" : new_user.email,
                    "firstName" : new_user.first_name,
                    "role" : new_user.role.name
                },
                "access_token": access_token
            })
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        

@auth.route('/api/admin/logout', methods=['POST'])
@jwt_required()
def api_admin_logout():
    flask_login.logout_user()
    return jsonify({"message": "You have been logged out"})

@auth.route('/api/user/logout', methods=['POST'])
@jwt_required()
def api_user_logout():
    flask_login.logout_user()
    return jsonify({"message": "You have been logged out"})

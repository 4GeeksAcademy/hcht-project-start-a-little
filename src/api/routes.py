"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
# from flask import Flask, request, jsonify, url_for, Blueprint
from flask import Flask, request, Blueprint, jsonify
from api.utils import generate_sitemap, APIException
from api.models import db, User


api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {"message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"}
    return response_body, 200


@api.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        users = db.session.execute(db.select(User).order_by(User.name)).scalars()
        results = [item.serialize() for item in users]
        response_body = {"message": "esteo develve el GET del endpoint /users",
                         "results": results,
                         "status": "ok"}
        return response_body, 200
    if request.method == 'POST':  # signup
        request_body = request.get_json()
        user = User(email = request_body["email"],
                    password = request_body["password"],
                    name = request_body["name"],
                    phone = request_body["phone"])
        db.session.add(user)
        db.session.commit()
        print(request_body)
        response_body = {"message": "Adding new user",
                         "status": "ok",
                         "new_user": request_body}
        return response_body, 200


@api.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(id):
    if request.method == 'GET':
        user = db.get_or_404(User, id)
        print(user)
        response_body = {"status": "ok",
                         "results": user.serialize()} 
        return response_body, 200
    if request.method == 'PUT':
        request_body = request.get_json()
        user = db.get_or_404(User, id)
        user.email = request_body["email"]
        user.password = request_body["password"]
        user.name = request_body["name"]
        user.phone = request_body["phone"]
        db.session.commit()
        response_body = {"message": "Updating user",
                         "status": "ok",
                         "user": request_body}
        return response_body, 200
    if request.method == 'DELETE':
        user = db.get_or_404(User, id)
        db.session.delete(user)
        db.session.commit()
        response_body = {"message": "Deleting user",
                         "status": "ok",
                         "user_deleting": id}
        return response_body, 200
        

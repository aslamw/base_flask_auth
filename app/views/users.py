from werkzeug.security import generate_password_hash
from app import db
from flask import request, jsonify
from ..models.users import Users, user_schema, users_schema

def post_user():
    username = request.json['username']
    password = request.json['password']
    name = request.json['name']
    email = request.json['email']
    pass_hash = generate_password_hash(password)
    user = Users(username, pass_hash, name, email)
    
    try:
        db.session.add(user)
        db.session.commit()
        result = user_schema.dump(user)
        
        return jsonify({'message': 'sucessfully registered', 'data': result}),201
    
    except:
        return jsonify({'message':'unablo to create'}),500

def update_user(id):
    username = request.json['username']
    password = request.json['password']
    name = request.json['name']
    email = request.json['email']
    
    user = Users.query.get(id)
    
    if not user:
        return jsonify({'massage':"user don't exist", 'data':{}}),404
    
    pass_hash = generate_password_hash(password)

    try:
        user.username = username
        user.password = pass_hash
        user.name = name
        user.email = email
        db.session.commit()
        result = user_schema.dump(user)
        
        return jsonify({'message':'sucessfully update','data':result}),202
    except:
        return jsonify({'message':'unable to update'}),500
    
def get_users():
    users = Users.query.all()
    
    if users:
        result = users_schema.dump(users)
        return jsonify({'messagae':'sucessfully fetched'}),200
    
    return jsonify({'message':'nothing found'}),500

def get_user(id):
    user = Users.query.get(id)
    
    if user:
        result = user_schema.dump(user)
        return jsonify({'message': 'sucessfully fetched', 'data':result}),200
    
    return jsonify({"message':'user don't exist"}),404

def delete_user(id):
    user = Users.query.get(id)
    
    if not user:
        return jsonify({'message':"user don't exist"}),404
    
    try:
        db.session.delete(user)
        db.session.commit()
        result = user_schema.dump(user)
        
        return jsonify({'message':'sucessfully delete user'}),200
    
    except:
        return jsonify({'message':'unable to delete'}),500
    
def user_by_username(username):
    try:
        return Users.query.filter(Users.username == username).one()
    
    except:
        return None
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify
from functools import wraps
from .users import user_by_username
from app import app
import jwt

def auth():
    auth = request.authorization
    
    if not auth or not auth.username or not auth.password:
        return jsonify({'message':'could not verify', 'Authenticate': 'Basic auth=login required'}),401
    
    user = user_by_username(auth.username)
    if not user:
        return jsonify({'message':'user not found'}),401
    
    if user and check_password_hash(user.password, auth.password):
        token = jwt.encode({'username':user.username, 'exp': datetime.now() + datetime.timedelta(hours=12)},
                          app.config['SECRET_KEY'])
        return jsonify({'message':'validated sucessfully', 'token': token.decode('UTF-8'), 'exp': datetime.now() + datetime.timedelta(hours=12)}), 200
        
    return jsonify({'message': 'could not verify', 'Authenticate': 'Basic auth="login required"'}),401

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        
        if not token:
            return jsonify({'message': 'token is missing'}),401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            curret_user = user_by_username(username=data['username'])
            
        except:
            return jsonify({'message': 'token is invalid or expired'}),401
        
        return f(curret_user, *args, **kwargs)
    
    return decorated
from flask import jsonify, request
from datetime import timedelta, datetime
import jwt
from models.models import *
from utils.utils import checktoken
import logging
import pymongo
from pymongo import UpdateOne
    
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')    



def login():
    data = request.get_json()
    user_email = data['user_email']
    user_password = data['user_password']
    doc = users.find_one({'user_email': user_email})
    if doc and doc['user_password'] == user_password:
        token = jwt.encode({'username': user_email}, datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), algorithm='HS256')
        response = {'valid': True, 'user_given_name': doc['user_given_name'], 'user_picture': "https://picsum.photos/200", 'user_token': token, 'user_email':user_email}
        entry = {
            "vallid": True,
            "token": token,
            "data": datetime.now().isoformat(),
            "user_email": user_email,
        }
        res = tokens.insert_one(entry)
        return jsonify(response), 200
    else:
        response = {'valid': False, 'error': 'Email or password incorrect.'}
        return jsonify(response), 400



def register():
    data = request.get_json()
    user_email = data['user_email'] 
    entry = {
        "user_full_name": data['user_full_name'],
        "user_given_name": data['user_given_name'],
        "user_email": user_email,
        "user_phone": data['user_phone'],
        "user_city": data['user_city'],
        "user_address": data['user_address'],
        "user_password": data['user_password'],
        "registration_time": datetime.now()
    }
    try:
        id = users.insert_one(entry).inserted_id
        token = jwt.encode({'username': entry['user_email']}, datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), algorithm='HS256')
        token_entry = {
            "token": token,
            "data": datetime.now().isoformat(),
            "user_email": entry['user_email'],
        }
        res = tokens.insert_one(token_entry)
        response = {'valid': True, 'session_token': token}, 200
    except pymongo.errors.DuplicateKeyError as description_error:
        response = {'valid': False, 'error': str(description_error)}, 400
    return jsonify(response), 400

def get_user_info():
    
    data    = request.get_json()
    token   = data['token']
    check   = checktoken(token)
    
    if check['valid'] == True:
        
        doc = users.find_one({'user_email' : check['email']})
        response = {
            'valid'            : True, 
            'user_given_name'   : doc['user_given_name'], 
            'user_full_name'    : doc['user_full_name'],
            'user_email'        : doc['user_email'],
            'user_password'     : doc['user_password'],
            'user_phone'        : doc['user_phone'],
            'user_city'         : doc['user_city'],
            'user_address'      : doc['user_address'],
            'user_picture'      : "https://picsum.photos/200",
            'token'        : token
        }
        
        return jsonify(response), 200
    
    else:
        response = {'valid': False, 'message': check['error']}, 400
    
    return jsonify(response), 400




        
        
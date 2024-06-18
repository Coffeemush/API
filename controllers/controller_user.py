from flask import jsonify, request
from datetime import timedelta, datetime
import jwt
from models.models import *
from utils.utils import checktoken
import logging
import pymongo
    
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')    



def login():
    data = request.get_json()
    user_email = data['user_email']
    user_password = data['user_password']
    doc = users.find_one({'user_email': user_email})
    if doc and doc['user_password'] == user_password:
        token = jwt.encode({'username': user_email}, datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), algorithm='HS256')
        response = {'valid': True, 'user_given_name': doc['user_given_name'], 'user_picture': "https://picsum.photos/200", 'token': token, 'user_email':user_email}
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
    doc = users.find_one({'user_email': user_email})
    if doc:
        return jsonify({'valid': False, 'error': f'email "{user_email}" already has an account'}), 400
    entry = {
        "user_surname": data['user_surname'],
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
        return jsonify({'valid': True, 'token': token}), 200
    except pymongo.errors.DuplicateKeyError as description_error:
        return jsonify(response = {'valid': False, 'error': str(description_error)}), 400

def get_user_info():
    token   = request.headers.get('token')
    logging.info(token)
    check   = checktoken(token)
    
    if check['valid'] == True:
        
        doc = users.find_one({'user_email' : check['email']})
        response = {
            'valid'            : True, 
            'user_given_name'   : doc['user_given_name'], 
            'user_surname'      : doc.get('user_surname'),
            'user_email'        : doc['user_email'],
            'user_phone'        : doc['user_phone'],
            'user_city'         : doc['user_city'],
            'user_address'      : doc['user_address'],
            'user_picture'      : "https://picsum.photos/200",
            'token'             : token
        }
        return jsonify(response), 200
    
    else:
        response = {'valid': False, 'message': check['error']}
    logging.info(response)
    return jsonify(response), 400

def edit_user():
    data = request.get_json()
    token   = data['token']
    check   = checktoken(token)
    if check['valid'] == True:
        user_email = data['user_email']
        doc = users.find_one({'user_email': user_email})
        if doc:
            try:
                logging.info(doc)
                if "user_surname" in data:
                    doc["user_surname"] = data['user_surname']
                if "user_given_name" in data:
                    doc["user_given_name"] = data['user_given_name']
                if "user_phone" in data:
                    doc["user_phone"] = data['user_phone']
                if "user_city" in data:
                    doc["user_city"] = data['user_city']
                if "user_address" in data:
                    doc["user_address"] = data['user_address']
                if "user_password" in data:
                    doc["user_password"] = data['user_password']
                result = users.update_one({'_id': doc['_id']}, {'$set': doc})
                if result.modified_count > 0:
                    return jsonify({'valid': True, 'token': token}), 200
                else:
                    return jsonify({'valid': False, 'error': 'No changes made'}), 400
            except pymongo.errors.DuplicateKeyError as description_error:
                return jsonify({'valid': False, 'error': str(description_error)}), 400
        return jsonify({'valid': False, 'error': "email not found"}), 400
    return jsonify(check), 400

from flask import jsonify, request
from models.models import *
from utils.utils import checktoken
import pymongo

def check_token():
    token   = request.headers.get('token')
    check = checktoken(token)
    if check["valid"] == True: 
        return jsonify(check), 200
    else:
        return jsonify(check), 400

def logout():
    data = request.get_json()
    try:
        tokens.delete_one({'token': data['token']})
        response = {'valid': True}
    except pymongo.errors.DuplicateKeyError as description_error:
        response = {'valid': False, 'error': str(description_error)}
    return jsonify(response), 200
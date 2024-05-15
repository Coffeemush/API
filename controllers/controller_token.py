from flask import jsonify, request
from models.models import *
from utils.utils import checktoken
import pymongo

def check_token():
    data = request.get_json()
    token = data['session_token']
    check = checktoken(token)
    return jsonify(check)

def logout():
    data = request.get_json()
    try:
        tokens.delete_one({'token': data['session_token']})
        response = {'valid': True}
    except pymongo.errors.DuplicateKeyError as description_error:
        response = {'valid': False, 'error': str(description_error)}
    return jsonify(response)
from flask import jsonify, request
from utils.utils import checktoken, get_data_for_graphic

from models.models import users, devices, SENSORS, devices_data
import logging
import json
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')    



def connect():
    # Needed parameters
    #   - token: Valid token
    #   - id: Valid coffeemush id
    #   - options: Valid options for subscription (beta)

    data = request.get_json()
    check = checktoken(data['token'])
    
    if check['valid']:
        try:
            doc = users.find_one({'user_email': check['email']})

            if 'connections' in doc:
                doc['connections'][data['id']] = json.loads(data['options'])
                users.update_one({'user_email': check['email']}, {'$set': doc})

            else:
                doc['connections'] = {data['id']: json.loads(data['options'])}
                users.update_one({'user_email': check['email']}, {'$set': doc})

            return jsonify({'valid': True}), 200
        
        except Exception as e:
            return jsonify({'valid': False, 'error': str(e)}) , 400  

    else:
        return jsonify(check), 400
    

def disconnect():
    # Needed parameters
    #   - token: Valid token
    #   - id: Valid coffeemush id

    data = request.get_json()
    check = checktoken(data['token'])
    
    if check['valid']:
        try:
            doc = users.find_one({'user_email': check['email']})

            if 'connections' in doc and [data['id']] in doc['connections']:
                del doc['connections'][data['id']]
                users.update_one({'user_email': check['email']}, {'$set': doc})
                return jsonify({'valid': True}), 200
            
            else:
                return jsonify({'valid': False, 'error': f"No connection with id '{data['id']}' found for user with email '{check['email']}'"}), 200
        
        except Exception as e:
            return jsonify({'valid': False, 'error': str(e)}), 400   

    else:
        return jsonify(check), 400
    

def get_data():
    # Needed parameters
    #   - token: Valid token
    data = request.get_json()
    check = checktoken(data['token'])
    
    if check['valid']:
        try:
            doc = users.find_one({'user_email': check['email']})
            answer = []
            if 'connections' in doc:
                for key, value in doc['connections'].items():
                    device = devices.find_one({'id': key})
                    
                    for sensor in SENSORS:
                        device[f'chart_{sensor}'] = get_data_for_graphic(key, sensor)
                    
                    answer.append(device)
                
                if len(answer) == 0:
                    return jsonify({'valid': False, 'error': 'No connected devices found for this user'}), 200
                    
                return jsonify({'valid': True, 'devices': answer}), 200

            else:
                return jsonify({'valid': False, 'error': f"No connection found for user with email '{check['email']}'"}), 200
        
        except Exception as e:
            return jsonify({'valid': False, 'error': str(e)}), 400   

    else:
        return jsonify(check), 400
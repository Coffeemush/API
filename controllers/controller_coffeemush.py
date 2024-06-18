from flask import jsonify, request, send_file
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
                try:
                    logging.info(f"data['options'] before json.loads: {data['options']}")
                    doc['connections'][data['id']] = json.loads(data['options'])
                except json.JSONDecodeError as e:
                    logging.error(f"JSONDecodeError: {str(e)} - Storing as string")
                    doc['connections'][data['id']] = data['options']
                except Exception as e:
                    logging.error(f"Unexpected error: {str(e)}")
                    return jsonify({'valid': False, 'error': str(e)}), 400
                users.update_one({'user_email': check['email']}, {'$set': doc})

            else:
                try:
                    logging.info(f"data['options'] before json.loads: {data['options']}")
                    doc['connections'] = {data['id']: json.loads(data['options'])}
                except json.JSONDecodeError as e:
                    logging.error(f"JSONDecodeError: {str(e)} - Storing as string")
                    doc['connections'] = {data['id']: data['options']}
                except Exception as e:
                    logging.error(f"Unexpected error: {str(e)}")
                    return jsonify({'valid': False, 'error': str(e)}), 400
                
                users.update_one({'user_email': check['email']}, {'$set': doc})

            return jsonify({'valid': True}), 200
        
        except Exception as e:
            logging.info(str(e))
            return jsonify({'valid': False, 'error': str(e)}) , 400  

    else:
        logging.info(check)
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

            if 'connections' in doc and data['id'] in doc['connections']:
                del doc['connections'][data['id']]
                users.update_one({'user_email': check['email']}, {'$set': doc})
                return jsonify({'valid': True}), 200
            
            else:
                return jsonify({'valid': False, 'error': f"No connection with id '{data['id']}' found for user with email '{check['email']}'"}), 200
        
        except Exception as e:
            logging.info(e)
            return jsonify({'valid': False, 'error': str(e)}), 400   

    else:
        return jsonify(check), 400
    

#def get_data():
#    # Needed parameters
#    #   - token: Valid token
#    token   = request.headers.get('token')
#    check = checktoken(token)
#    
#    if check['valid']:
#        try:
#            doc = users.find_one({'user_email': check['email']})
#            answer = []
#            if 'connections' in doc:
#                for key, value in doc['connections'].items():
#                    device = devices.find_one({'id': key})
#                    
#                    for sensor in SENSORS:
#                        device[f'chart_{sensor}'] = get_data_for_graphic(key, sensor)
#                    
#                    answer.append(device)
#                
#                if len(answer) == 0:
#                    return jsonify({'valid': False, 'error': 'No connected devices found for this user'}), 200
#                    
#                return jsonify({'valid': True, 'devices': answer}), 200
#
#            else:
#                return jsonify({'valid': False, 'error': f"No connection found for user with email '{check['email']}'"}), 200
#        
#        except Exception as e:
#            logging.info(e)
#            return jsonify({'valid': False, 'error': str(e)}), 400   
#
#    else:
#        return jsonify(check), 400

def get_data():
    # Needed parameters
    #   - token: Valid token
    #   - id(optional): id of a device (if there is no this field it just returns all devices)
    #   - sensor: sensor type (if there is no this field it does not return history data for the device)
    token = request.headers.get('token')
    id = request.headers.get('id')
    sensor = request.headers.get('sensor')
    check = checktoken(token)
    
    if check['valid']:
        try:                    
            doc = users.find_one({'user_email': check['email']})
            
            if id is not None:
                if 'connections' not in doc or id not in doc['connections']:
                    return jsonify({"valid": False, "error": "You are not connected to this device"}), 200
                
                device = devices.find_one({'id': id})
                
                if device is None:
                    return jsonify({"valid": False, "error": "Device not found in database"}), 200
                    
                if sensor is None:
                    if 'name' not in device:
                        device['name'] = id
                    if '_id' in device:
                        del device['_id']
                    return jsonify({"valid": True, "device": device}), 200
                
                else:
                    period = request.headers.get('period')
                    if period is None:
                        period = 'day'
                    startDate = request.headers.get('startDate')
                    endDate = request.headers.get('endDate')
                    buf = get_data_for_graphic(id, sensor, period, [startDate, endDate])
                    return send_file(buf, mimetype='image/png', as_attachment=False, attachment_filename='plot.png')
            if 'connections' in doc:
                logging.info(doc['connections'])
                for key, value in doc['connections'].items():
                    device = devices.find_one({'id': key})
                    logging.info(" ", device)
                    if device is not None:
                        if 'name' in device:
                            answer.append(device['name'])
                        else:
                            answer.append(key)
                
                if len(answer) == 0:
                    return jsonify({'valid': False, 'error': 'No connected devices found for this user'}), 200
                    
                return jsonify({'valid': True, 'devices': answer}), 200

            else:
                return jsonify({'valid': False, 'error': f"No connection found for user with email '{check['email']}'"}), 200
        
        except Exception as e:
            logging.info(e)
            return jsonify({'valid': False, 'error': str(e)}), 400   

    else:
        return jsonify(check), 400
    
def updateName():
    # Needed parameters
    #   - token: Valid token
    #   - id: Valid coffeemush id
    #   - name: New name for device

    data = request.get_json()
    check = checktoken(data['token'])
    
    if check['valid']:
        try:
            doc = users.find_one({'user_email': check['email']})
            id = data['id']
            if 'connections' in doc and id in doc['connections']:
                device = devices.find_one({'id': id})
                device['name'] = data['name']
                devices.update_one({'id': id}, {'$set': device})
            return jsonify({'valid': True}), 200
        
        except Exception as e:
            logging.info(str(e))
            return jsonify({'valid': False, 'error': str(e)}) , 400  

    else:
        logging.info(check)
        return jsonify(check), 400

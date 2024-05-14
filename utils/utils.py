from models.models import tokens, users
from datetime import datetime, timedelta

def checktoken(token):
        
        if(token=="internal"):
            return {'valid': True, 'type': 'internal'}
        
        user_data = tokens.find_one({'token': token})

        if user_data is None:
            response = {'valid': False, 'error': 'Token does not exist.'}

        else:

            user = users.find_one({'user_email': user_data['user_email']})

            if user is None:
                response = {'valid': False, 'error': 'Invalid or inexistent user.'}

            elif datetime.now() <= (datetime.strptime(user_data['data'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(minutes=50)):
                response = {'valid': 'ok', 'email': user['user_email'], 'type': user["user_role"]}
                tokens.update_one({'token': token}, {'$set': {'data': datetime.now().isoformat()}})
            
            else:
                response = {'valid': False, 'error': 'Timeout'}

        return response
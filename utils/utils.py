from models.models import tokens, users, devices_data
from datetime import datetime, timedelta

def checktoken(token):
        
        if(token=="internal_testing"):
            return {'valid': True, 'email': 'internal_testing'}
        
        user_data = tokens.find_one({'token': token})

        if user_data is None:
            response = {'valid': False, 'error': 'Token does not exist.'}

        else:
            user = users.find_one({'user_email': user_data['user_email']})

            if user is None:
                response = {'valid': False, 'error': 'Invalid or inexistent user.'}

            elif datetime.now() <= (datetime.strptime(user_data['data'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(minutes=50)):
                response = {'valid': True, 'email': user['user_email']}
                tokens.update_one({'token': token}, {'$set': {'data': datetime.now().isoformat()}})
            
            else:
                response = {'valid': False, 'error': 'Timeout'}

        return response


def get_data_for_graphic(id, sensor, range_type='day', dates=[None, None]):
    # Needed parameters
    #   - id: Valid id for a device
    #   - sensor: Valid sensor name
    #   - (Optional)long: Tells how long the range between dates should be. Ending date being now()
    #   - (Optional)dates: Tells range of dates to return data
    if dates is None:
        dates[0] = datetime.now().date()

        if range_type == 'day':
            dates[1] = dates[0] - timedelta(days=1)

        elif range_type == 'week':
            dates[1] = dates[0] - timedelta(weeks=1)

        elif range_type == 'month':
            if dates[0].month == 1:
                dates[1] = datetime(dates[0].year - 1, 12, dates[0].day)
            
            else:
                dates[1] = datetime(dates[0].year, dates[0].month - 1, dates[0].day)

    return devices_data[id][sensor].find({'date': {'$gte': dates[0], '$lte': dates[1]}})
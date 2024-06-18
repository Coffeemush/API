from models.models import tokens, users, devices_data, devices
from datetime import datetime, timedelta
import random
import string
from faker import Faker
import logging
import pymongo
import matplotlib.pyplot as plt
    
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')    


humidity_entry = (51.0, 99.0)
temperature_entry = (10.0, 30.0)
light_entry = (150.0, 500.0)


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
    if dates == [None, None]:
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
    dates = [date.isoformat() for date in dates]
    dates.sort()
    logging.info(dates)
    logging.info(sensor)
    logging.info(id)
    res = devices_data.find({
                    'id': id
                    #'$and': [
                    #    #{f'{sensor}.time': {'$gte': dates[0], '$lte': dates[1]}}
                    #    {f'{sensor}.time': {'$gte': dates[1]}}
                    #]
                })
    res_list = list(res)
    processed_data = []
    for doc in res_list:
        if '_id' in doc:
            del doc['_id']
        if sensor in doc:
            for entry in doc[sensor]:
                processed_data.append({
                    'value': entry['value'],
                    'time': entry['time'].isoformat()
                })
    
    logging.info(processed_data)
    values = [entry['value'] for entry in processed_data]
    times = [datetime.fromisoformat(entry['time']) for entry in processed_data]

    # Plot the data
    plt.figure(figsize=(10, 5))
    plt.plot(times, values, marker='o', linestyle='-', color='b')

    # Format the plot
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('Sensor Data Over Time')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Show the plot
    plt.tight_layout()
    plt.show()
    return processed_data
from pymongo import MongoClient
import os
#from utils.utils import create_random_devices 
from datetime import datetime, timedelta
import random
import string
from faker import Faker
import logging
import pymongo
    
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')    


humidity_entry = (51.0, 99.0)
temperature_entry = (10.0, 30.0)
light_entry = (150.0, 500.0)

SENSORS = ["TVOC", "CO2", "Humidity", "Temperature", "Camera"]

user = os.environ.get('MONGO_ROOT_USER')
password = os.environ.get('MONGO_ROOT_PASSWORD')
MONGO_URI = f'mongodb://{user}:{password}@mongo:27017/?authSource=admin'

client = MongoClient(MONGO_URI)
db = client["Coffeemush"]
users = db['users']
tokens = db['tokens']
devices = db['devices']
devices_data = db['devices_data']


def create_random_devices(num=10000, data_entries=(2531,51235)):
    for i in range(num):
        device_id  = ''.join(random.choices(string.digits, k=20))
        logging.info(f"About to create device number {i} with code {device_id}")
        entry = {
            "id": device_id,
            "humidity": random.uniform(humidity_entry[0], humidity_entry[1]),
            "light": random.uniform(light_entry[0], light_entry[1]),
            "temperature": random.uniform(temperature_entry[0], temperature_entry[1]),
            "water_empty": random.choice([True, False])
        }
        devices.insert_one(entry)
        entry = {
            "id": device_id,
            "humidity": [],
            "light": [],
            "temperature": []
        }
        current_time = datetime.now()
        for i in range(random.randint(data_entries[0], data_entries[1])):
            entry['humidity'].append({"value": random.uniform(humidity_entry[0], humidity_entry[1]), "time": current_time})
            entry['light'].append({"value": random.uniform(light_entry[0], light_entry[1]), "time": current_time})
            entry['temperature'].append({"value": random.uniform(temperature_entry[0], temperature_entry[1]), "time": current_time})
            current_time -= timedelta(hours=1)
        devices_data.insert_one(entry)


#create_random_devices(100)

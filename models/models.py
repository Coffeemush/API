from pymongo import MongoClient
import os

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




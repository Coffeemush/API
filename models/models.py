from pymongo import MongoClient
from app import app
import os

user = os.environ.get('MONGO_ROOT_USER')
password = os.environ.get('MONGO_ROOT_PASSWORD')
MONGO_URI = f'mongo://{user}:{password}@mongodb:27017/?authSource=admin'

client = MongoClient(MONGO_URI)
db = client["Coffeemush"]
users = db['users']




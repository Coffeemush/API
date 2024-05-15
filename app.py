from flask import Flask
import os
from flask_mqtt import Mqtt
from routes.routes import *
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')    


logging.info("Starting app...")

app = Flask(__name__)

app.config['MQTT_BROKER_URL'] = os.environ.get('MQTT_BROKER_URL')
app.config['MQTT_BROKER_PORT'] = int(os.environ.get('MQTT_BROKER_PORT'))
#app.config['MQTT_USERNAME'] = os.environ.get('MQTT_USERNAME')
#app.config['MQTT_PASSWORD'] = os.environ.get('MQTT_PASSWORD')
app.config['MQTT_KEEPALIVE'] = int(os.environ.get('MQTT_KEEPALIVE'))
if os.environ.get('MQTT_TLS_ENABLED') == 'False':
    app.config['MQTT_TLS_ENABLED'] = False
else:
    app.config['MQTT_TLS_ENABLED'] = True
topic = os.environ.get('TOPIC')
mqtt = Mqtt(app)

routes_user(app)
routes_coffeemush(app)
routes_token(app)
routes_mqtt(mqtt, topic)
#test
@app.route('/')
def index():
    return 'Connected to MongoDB!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
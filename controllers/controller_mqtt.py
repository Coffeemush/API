from flask_mqtt import Mqtt
import logging
from datetime import datetime
import base64
import binascii
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')    

def handle_connect(mqtt, topics):
    @mqtt.on_connect()
    def handle_connect(client, userdata, flags, rc):
        mqtt.subscribe('CM1')
        for topic in topics:
            logging.info(f"Subscribing to topic '{topic}'...")
            mqtt.subscribe(topic)
            logging.info("Subscribtion finished.")
            #for top in ['sensor/temperature', 'sensor/humidity', 'sensor/light', 'sensor/float_switch']:
            #    mqtt.subscribe(top)


def handle_mqtt_message(mqtt):
    @mqtt.on_message()
    def handle_mqtt_message(client, userdata, message):
        if message.topic == 'device1/sensors':
            pass
        elif message.topic == 'device1/event':
            pass
        elif message.topic == 'CM1/CAM':
            now = datetime.now()
            filename = now.strftime("%m%d%Y-%H%M%S.jpg")
            filepath = ".debug/" + filename
            
            try:
                with open(filepath, 'wb') as f:
                    f.write(message.payload)
                logging.info(f"Image saved to {filepath}")
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
        
        logging.info("Message received.")
        logging.info(message)
        logging.info(message.topic)
        logging.info(message.payload)

# Example usage
# Assuming `mqtt` is your MQTT client instance
# handle_mqtt_message(mqtt)
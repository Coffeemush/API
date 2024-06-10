from flask_mqtt import Mqtt
import logging
from datetime import datetime
import base64
import binascii
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')    

def handle_connect(mqtt, topics):
    @mqtt.on_connect()
    def handle_connect(client, userdata, flags, rc):
        mqtt.subscribe('cm/picture')
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
        elif message.topic == 'cm/picture':
            now = datetime.now()
            filename = now.strftime("%m%d%Y-%H%M%S.jpg")
            f = open(".debug/" + filename, 'wb')
            
            # Ensure proper padding
            img_data = message.payload
            missing_padding = len(img_data) % 4
            if missing_padding:
                img_data += b'=' * (4 - missing_padding)
            
            try:
                final_img = base64.b64decode(img_data)
                f.write(final_img)
            except binascii.Error as e:
                logging.error(f"Error decoding base64 data: {e}")
            finally:
                f.close()
        
        logging.info("Message received.")
        logging.info(message)
        logging.info(message.topic)
        logging.info(message.payload)
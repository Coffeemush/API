from flask_mqtt import Mqtt
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')    

def handle_connect(mqtt, topic):
    @mqtt.on_connect()
    def handle_connect(client, userdata, flags, rc):
        logging.info(f"Subscribing to topic '{topic}'...")
        mqtt.subscribe(topic)
        logging.info("Subscribtion finished.")


def handle_mqtt_message(mqtt):
    @mqtt.on_message()
    def handle_mqtt_message(client, userdata, message):
        logging.info("Message received.")
        data = dict(
            topic=message.topic,
            payload=message.payload.decode()
        )
        logging.info(data)
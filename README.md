# API

# Broker

    # Publish a message to a topic
    mosquitto_pub -h localhost -t "your/topic" -m "Hello, MQTT!"

    # Subscribe to a topic to receive messages
    mosquitto_sub -h localhost -t "your/topic"

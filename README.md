# API

# Broker

    # Command to publish a message to the topic flask/mqtt
    mosquitto_pub -h localhost -p 1884 -t "flask/mqtt" -m "Hello, MQTT!"

    # Command to subscribe to the previous topic
    mosquitto_sub -h localhost -p 1884 -t "flask/mqtt"

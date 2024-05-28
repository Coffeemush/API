# API

# Broker

    # Command to publish a message to the topic flask/mqtt
    mosquitto_pub -h localhost -p 1884 -t "flask/mqtt" -m "Hello, MQTT!"

    # Command to subscribe to the previous topic
    mosquitto_sub -h localhost -p 1884 -t "flask/mqtt"

    # Testing broker efficiency
    docker run --rm inovex/mqtt-stresser -broker tcp://wouterpeetermans.com:1884 -num-clients 10 -num-messages 150 -rampup-delay 1s -rampup-size 10 -global-timeout 180s -timeout 20s

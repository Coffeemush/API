# API

# Broker

    # Command to publish a message to the topic flask/mqtt
    mosquitto_pub -h localhost -p 1884 -t "flask/mqtt" -m "Hello, MQTT!"

    # Command to subscribe to the previous topic
    mosquitto_sub -h localhost -p 1884 -t "flask/mqtt"

    # Testing broker efficiency
    docker run --rm inovex/mqtt-stresser -broker tcp://wouterpeetermans.com:1884 -num-clients 10 -num-messages 150 -rampup-delay 1s -rampup-size 10 -global-timeout 180s -timeout 20s



# From the server i can publish the following messages to the device1/server topic:

    ##  {
            "type": "variables", 
            "variables": {
                "active": "0"/"1",
                //Other variables i can send once u have ur variables
            }
    } // this means you need to set the variables as i send it to you in the variables key which contains another json
    ##  {
            "type": "request",
            "reason": "picture"
    }   // This means u have to publish a picture to the "device1/sensors" (just the picture)
    ##  {
            "type": "request",
            "reason": "sensors"
    }   // This means u have to publish a json with all sensor values to the "device1/sensors"
    ##  {
        
    }




# From the server i can receive the following messages to the device1/event topic:

    ##  {
            "type": "notification",
            "reason": "water_level"
    }
    ##  {
            "type": "notification",
            "reason": "much_light"
    }
    ##  {
            "type": "ini"
    }
    ##  {
            "type": "request",
            "reason": "image_name"
    }


# From the server i can receive the following messages to the device1/sensors topic:

    ##  {
            "time": whatever //mandatory
            "temperature": whatever //optional
            "humidity": whatever //optional
            "light": whatever //optional
            "water": whatever //optional
            "picture": whatever //optional
    } // this is how u send me data, not all sensors have to be at once, but i can accept all of this

    ## {
        "name": "elfkhewgi9", //two bytes is enough
        "order": "13", // two bytes
        "bytes": whatever //124 bytes
    }
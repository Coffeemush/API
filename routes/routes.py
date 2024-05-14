
from controllers.controller_mqtt import *
from controllers.controller_user import *
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')    

def routes_user(app):
    app.route("/api/login", methods=['POST'])(login)
    app.route("/api/register", methods=['POST'])(register)
    app.route("/api/checktoken", methods=['POST'])(check_token)
    app.route("/api/user_info", methods=['GET'])(get_user_info)
    app.route("/api/logout", methods=['POST'])(logout)

def routes_mqtt(mqtt, topic):
    logging.info("Connecting mqtt...")
    handle_connect(mqtt, topic)
    handle_mqtt_message(mqtt)


from controllers.controller_mqtt import *
from controllers.controller_user import *
from controllers.controller_coffeemush import *
from controllers.controller_token import *
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')    

def routes_user(app):
    app.route("/api/login", methods=['POST'])(login)
    app.route("/api/login", methods=['PUT'])(register)
    app.route("/api/user", methods=['GET'])(get_user_info)

def routes_token(app):
    app.route("/api/auth", methods=['GET'])(check_token)
    app.route("/api/auth", methods=['DELETE'])(logout)

def routes_coffeemush(app):
    app.route("/api/connection", methods=['POST'])(connect)
    app.route("/api/connection", methods=['DELETE'])(disconnect)
    app.route("/api/connection", methods=['GET'])(get_data)

def routes_mqtt(mqtt, topic):
    logging.info("Connecting mqtt...")
    handle_connect(mqtt, topic)
    handle_mqtt_message(mqtt)

from controllers.controller_mqtt import *
from controllers.controller_user import *

def routes_user(app):
    app.route("/api/login", methods=['POST'])(login)
    app.route("/api/register", methods=['POST'])(register)
    app.route("/api/checktoken", methods=['POST'])(check_token)
    app.route("/api/user_info", methods=['POST'])(get_user_info)
    app.route("/api/logout", methods=['POST'])(logout)
    app.route("/api/set_user_info", methods=['POST'])(set_user_info)

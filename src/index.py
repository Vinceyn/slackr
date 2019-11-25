"""Flask server"""
import sys
import os
from datetime import datetime
from flask_cors import CORS
from json import dumps
from flask import Flask, request

from server.auth import auth_blueprint
from server.user import user_blueprint
from server.users import users_blueprint
from server.admin import admin_blueprint
from server.search import search_blueprint
from server.message import message_blueprint
from server.standup import standup_blueprint
from server.channel import channel_blueprint
from server.channels import channels_blueprint

from server.reset import resets, reset_config
from server.handlers import ValueError_handler, AccessError_handler

from model.errors import AccessError
from datastore import store

## Application config
APP = Flask(__name__,
            static_url_path="",
            static_folder="../static")

APP.register_error_handler(ValueError, ValueError_handler)
APP.register_error_handler(AccessError, AccessError_handler)

CORS(APP)

## Register blueprints
APP.register_blueprint(auth_blueprint, url_prefix="/auth")
APP.register_blueprint(user_blueprint, url_prefix="/user")
APP.register_blueprint(users_blueprint, url_prefix="/users")
APP.register_blueprint(admin_blueprint, url_prefix="/admin")
APP.register_blueprint(search_blueprint, url_prefix="/search")
APP.register_blueprint(message_blueprint, url_prefix="/message")
APP.register_blueprint(standup_blueprint, url_prefix="/standup")
APP.register_blueprint(channel_blueprint, url_prefix="/channel")
APP.register_blueprint(channels_blueprint, url_prefix="/channels")

reset_config(APP)
APP.register_blueprint(resets, url_prefix="/auth/passwordreset")

## Echo routes
@APP.route('/echo/get', methods=['GET'])
def echo1():
    """ Description of function """
    return dumps({
        'echo' : request.args.get('echo'),
    })

@APP.route('/echo/post', methods=['POST'])
def echo2():
    """ Description of function """
    return dumps({
        'echo' : request.form.get('echo'),
    })

@APP.route('/debug/show', methods=['GET'])
def show_store():
    return store.s

## Run server
if __name__ == '__main__':
    # Check if there is an existing version of the datastore
    if "noload" not in sys.argv:
        states = os.listdir("../data")
        if states:
            file_name = max(states)
            print(f"[index.py] Found earlier datastore state {file_name}; loading")

            store.restore(os.path.abspath(f"../data/{file_name}"))
        else:
            print("[index.py] No pre-existing datastore state found; skipping load")

    # Listen for connections
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))

    # Save the datastore
    if "save" in sys.argv:
        out_file_name = str(int(datetime.timestamp(datetime.now()))) + ".p"
        print(f"[index.py] Saving current datastore state as {out_file_name}")
        store.save(os.path.abspath(f"../data/{out_file_name}"))


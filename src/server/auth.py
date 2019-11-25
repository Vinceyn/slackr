from flask import Blueprint, request
from json import dumps

from model.auth import *

# Initialise blueprint
auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("login", methods=["POST"])
def login():
	return auth_login(request.form.get("email"), request.form.get("password"))

@auth_blueprint.route("logout", methods=["POST"])
def logout():
	return auth_logout(request.form.get("token"))

@auth_blueprint.route("register", methods=["POST"])
def register():
	return auth_register(
			request.form.get("email"),
			request.form.get("password"),
			request.form.get("name_first"),
			request.form.get("name_last")
	)

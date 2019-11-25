from flask import Blueprint, request
from json import dumps

from model.user import user_all

# Initialise blueprint
users_blueprint = Blueprint("users", __name__)

@users_blueprint.route("/all", methods=["GET"])
def get_all():
	return user_all(request.args.get("token"))

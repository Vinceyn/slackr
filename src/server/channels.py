from flask import Blueprint, request
from json import dumps

from model.channel import *

# Initialise blueprint
channels_blueprint = Blueprint("channels", __name__)

@channels_blueprint.route("list", methods=["GET"])
def list():
	return channels_list(
		request.args.get("token")
	)

@channels_blueprint.route("listall", methods=["GET"])
def listall():
	return channels_listall(
		request.args.get("token")
	)

@channels_blueprint.route("create", methods=["POST"])
def create():
	return channels_create(
		request.form.get("token"),
		request.form.get("name"),
		(request.form.get("is_public") == "true")
	)
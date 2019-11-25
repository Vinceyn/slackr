from flask import Blueprint, request
from json import dumps

from model.standup import *

# Initialise blueprint
standup_blueprint = Blueprint("standup", __name__)

@standup_blueprint.route("start", methods=["POST"])
def start():
	return standup_start(
		request.form.get("token"),
		int(request.form.get("channel_id")),
		int(request.form.get("length"))
	)

@standup_blueprint.route("active", methods=["GET"])
def active():
	return standup_active(
		request.args.get("token"),
		int(request.args.get("channel_id"))
	)

@standup_blueprint.route("send", methods=["POST"])
def send():
	return standup_send(
		request.form.get("token"),
		int(request.form.get("channel_id")),
		request.form.get("message")
	)
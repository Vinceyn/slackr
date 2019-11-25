from flask import Blueprint, request
from json import dumps
from datetime import datetime as dt

from model.message import *

# Initialise blueprint
message_blueprint = Blueprint("message", __name__)

@message_blueprint.route("sendlater", methods=["POST"])
def sendlater():
	return (message_send_later(
		request.form.get("token"),
		int(request.form.get("channel_id")),
		request.form.get("message"),
		dt.fromtimestamp(int(request.form.get("time_sent"))))
	)

@message_blueprint.route("send", methods=["POST"])
def send():
	return(message_send(
		request.form.get("token"),
		int(request.form.get("channel_id")),
		request.form.get("message"))
	)

@message_blueprint.route("remove", methods=["DELETE"])
def remove():
	return message_remove(
		request.form.get("token"),
		int(request.form.get("message_id"))
	)

@message_blueprint.route("edit", methods=["PUT"])
def edit():
	return message_edit(
		request.form.get("token"),
		int(request.form.get("message_id")),
		request.form.get("message")
	)

@message_blueprint.route("react", methods=["POST"])
def react():
	return message_react(
		request.form.get("token"),
		int(request.form.get("message_id")),
		int(request.form.get("react_id"))
	)

@message_blueprint.route("unreact", methods=["POST"])
def unreact():
	return message_unreact(
		request.form.get("token"),
		int(request.form.get("message_id")),
		int(request.form.get("react_id"))
	)

@message_blueprint.route("pin", methods=["POST"])
def pin():
	return message_pin(
		request.form.get("token"),
		int(request.form.get("message_id"))
	)

@message_blueprint.route("unpin", methods=["POST"])
def unpin():
	return message_unpin(
		request.form.get("token"),
		int(request.form.get("message_id"))
	)

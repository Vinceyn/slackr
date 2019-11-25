from flask import Blueprint, request
from json import dumps

from model.channel import *

# Initialise blueprint
channel_blueprint = Blueprint("channel", __name__)

@channel_blueprint.route("invite", methods=["POST"])
def invite():
	return channel_invite(
		request.form.get("token"),
		int(request.form.get("channel_id")),
		int(request.form.get("u_id"))
	)

@channel_blueprint.route("details", methods=["GET"])
def details():
	return channel_details(
		request.args.get("token"),
		int(request.args.get("channel_id"))
	)

@channel_blueprint.route("messages", methods=["GET"])
def messages():
	return channel_messages(
		request.args.get("token"),
		int(request.args.get("channel_id")),
		int(request.args.get("start"))
	)

@channel_blueprint.route("leave", methods=["POST"])
def leave():
	return channel_leave(
		request.form.get("token"),
		int(request.form.get("channel_id"))
	)

@channel_blueprint.route("join", methods=["POST"])
def join():
	return channel_join(
		request.form.get("token"),
		int(request.form.get("channel_id"))
	)

@channel_blueprint.route("addowner", methods=["POST"])
def addowner():
	return channel_addowner(
		request.form.get("token"),
		int(request.form.get("channel_id")),
		int(request.form.get("u_id"))
	)

@channel_blueprint.route("removeowner", methods=["POST"])
def removeowner():
	return channel_removeowner(
		request.form.get("token"),
		int(request.form.get("channel_id")),
		int(request.form.get("u_id"))
	)

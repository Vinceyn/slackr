from flask import Blueprint, request
from json import dumps

from model.user import *

# Initialise blueprint
user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/profile", methods=["GET"])
def get_profile():
	return user_profile(request.args.get("token"), int(request.args.get("u_id")))

@user_blueprint.route("/profile/setemail", methods=["PUT"])
def set_email():
	return user_profile_setemail(request.form.get("token"), request.form.get("email"))

@user_blueprint.route("/profile/setname", methods=["PUT"])
def set_name():
	return user_profile_setname(request.form.get("token"), request.form.get("name_first"), request.form.get("name_last"))

@user_blueprint.route("/profile/sethandle", methods=["PUT"])
def set_handle():
	return user_profile_sethandle(request.form.get("token"), request.form.get("handle_str"))

@user_blueprint.route("/profiles/uploadphoto", methods=["POST"])
def set_img():
	return user_profiles_uploadphoto(
		request.form.get("token"),
		request.form.get("img_url"),
		int(request.form.get("x_start")),
		int(request.form.get("y_start")),
		int(request.form.get("x_end")),
		int(request.form.get("y_end")),
	)

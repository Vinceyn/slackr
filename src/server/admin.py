from flask import Blueprint, request
from json import dumps

from model.admin_userpermission_change import admin_userpermission_change

# Initialise blueprint
admin_blueprint = Blueprint("admin", __name__)

@admin_blueprint.route("/userpermission/change", methods=["POST"])
def userpermission_change():
	return admin_userpermission_change(request.form.get("token"),
		int(request.form.get("u_id")),
		int(request.form.get("permission_id"))
	)

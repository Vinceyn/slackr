from flask import Blueprint, request
from json import dumps

from model.search import *

# Initialise blueprint
search_blueprint = Blueprint("search", __name__)

@search_blueprint.route("/", methods=["GET"])
def search_route():
	return search(
		request.args.get("token"),
		request.args.get("query_str")
	)
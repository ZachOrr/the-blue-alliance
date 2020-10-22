from backend.tasks_io.tbans.main import ping, verify
from flask import Blueprint


blueprint = Blueprint('tbans', __name__)
blueprint.add_url_rule("/ping", view_func=ping)
blueprint.add_url_rule("/verify", view_func=verify)

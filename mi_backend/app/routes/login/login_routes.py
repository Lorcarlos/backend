from flask import Blueprint, request
from ...services.login.login_service import login

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["POST"])
def login_route():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    return login(username, password)
    
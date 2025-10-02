from flask import Blueprint, request
from ...services.login.login_service import login

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST", "OPTIONS"])
def login_route():
    if request.method == "OPTIONS":
       
        return {}, 200

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    return login(username, password)

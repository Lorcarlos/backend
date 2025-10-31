from flask import Blueprint, jsonify, request
from ...services.login_logs.user_logins_service import UserLoginsService
from ...services.log.log_service import LogService
from utils.decorators import role_required

user_logins_bp = Blueprint("user_logins_bp", __name__, url_prefix="/user-logins")

@user_logins_bp.route("/", methods=["GET", "OPTIONS"])
@role_required([1])
def get_all_user_logins():
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    try:
        user_logins = UserLoginsService.get_all_users_logins()
        return jsonify({"ok": True, "users_logins": user_logins}), 200
    except Exception as e:
        LogService.create_log({
            "module": f"{__name__}.{get_all_user_logins.__name__}",
            "message": f"Exception error {str(e)}",
        })
        return jsonify({"ok": False, "error": str(e)}), 500

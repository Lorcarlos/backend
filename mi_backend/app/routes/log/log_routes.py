from flask import Blueprint, jsonify, request
from ...services.log.log_service import LogService
from utils.decorators import role_required

# ✅ Prefijo del Blueprint
log_bp = Blueprint("log", __name__, url_prefix="/logs")

# ✅ Aceptamos GET y OPTIONS (para CORS preflight)
@log_bp.route("", methods=["GET", "OPTIONS"])
@log_bp.route("/", methods=["GET", "OPTIONS"])
@role_required([1])
def get_logs():
    # 🟢 Si es una solicitud de preflight (OPTIONS), respondemos sin error
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    try:
        logs = LogService.get_all_logs()
        return jsonify({"ok": True, "logs": logs}), 200

    except Exception as e:
        LogService.create_log({
            "module": f"{__name__}.{get_logs.__name__}",
            "message": f"Exception error {str(e)}",
        })
        return jsonify({"ok": False, "error": str(e)}), 500


@log_bp.route("/<int:id_log>", methods=["GET", "OPTIONS"])
@role_required([1])
def get_log(id_log):
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    try:
        if id_log <= 0:
            return jsonify({"ok": False, "error": "El id ingresado debe ser positivo"}), 400

        log = LogService.get_log_by_id(id_log)
        return jsonify({"ok": True, "log": log}), 200

    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 404

    except Exception as e:
        LogService.create_log({
            "module": f"{__name__}.{get_log.__name__}",
            "message": f"Exception error {str(e)}",
        })
        return jsonify({"ok": False, "error": str(e)}), 500


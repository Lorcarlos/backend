from flask import Blueprint, jsonify
from ...services.log.log_service import LogService

log_bp = Blueprint("log", __name__, url_prefix="/logs")


@log_bp.route("/", methods=["GET"])
def get_logs():
    try:

        logs = LogService.get_all_logs()

        return jsonify({"ok": True, "logs": logs}), 200

    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{get_logs.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"ok": False, "error": str(e)}), 500


@log_bp.route("/<id_log>", methods=["GET"])
def get_log(id_log):
    try:

        id_log = int(id_log)
        if id_log <= 0:
            return (
                jsonify({"ok": False, "error": "El id ingresado debe ser positivo"}),
                400,
            )

        log = LogService.get_log_by_id(id_log)

        return jsonify({"ok": True, "log": log}), 200

    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 404

    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{get_log.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"ok": False, "error": str(e)}), 500

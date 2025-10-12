from flask import Blueprint, jsonify
from app.database import get_connection
from ...services.log.log_service import LogService
permissions_bp = Blueprint("permissions", __name__)

@permissions_bp.route("/permissions", methods=["GET"])
def get_permissions():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(const.roles)  
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rows), 200
    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{get_permissions.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"error": str(e)}), 500

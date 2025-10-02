from flask import Blueprint, jsonify
from app.database import get_connection
product_bp = Blueprint("product", __name__)

@product_bp.route("/permissions", methods=["GET"])
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
        return jsonify({"error": str(e)}), 500

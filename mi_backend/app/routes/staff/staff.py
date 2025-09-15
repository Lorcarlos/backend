# app/routes/personal.py
from validator import validator
from flask import Blueprint, jsonify, request
from ...models.staff.staff import get_personal_data, insert_personal_data

personal_bp = Blueprint("personal", __name__)

@personal_bp.route("/", methods=["GET"])
def get_personal():
    try:
        data = get_personal_data()
        return jsonify({"ok": True, "personal": data}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500



personal_bp = Blueprint("personal", __name__)



@personal_bp.route("/create", methods=["POST"])
def create_personal():
    try:
        data = request.json
        required_fields = {
            "name": str,
            "phone": str,
            "email": str,
            "address": str
        }
        validator(data, required_fields)
        
        last_id = create_personal(data)
        
        return jsonify({"ok": True, "id": last_id}), 201
    
    except (ValueError, TypeError) as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"ok": False, "error": "Error del servidor: " + str(e)}), 500
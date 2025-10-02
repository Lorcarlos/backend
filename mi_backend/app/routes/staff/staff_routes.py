from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from ...database import db
from ...models.staff.staff_peticion import AppUser
from ...services.staff.staff import (
    get_user_by_id,
    create_new_user,
    soft_delete_user_if_requested,
    update_user_service,
)
from ...validator.validator import validate_data


personal_bp = Blueprint("personal_bp", __name__)


@personal_bp.route("/users", methods=["GET"])
def get_all_users():
    try:
        users = AppUser.query.filter_by(deleted_at=None).all()

        users_list = []
        for user in users:
            users_list.append(
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "username": user.username,
                    "document_id": user.document_id,
                    "phone_number": user.phone_number,
                    "role_id": user.role_id,
                    "branch_id": user.branch_id,
                    "is_active": user.is_active,
                    "created_at": user.created_at.isoformat(),
                    "updated_at": user.updated_at.isoformat(),
                }
            )

        return jsonify({"ok": True, "users": users_list}), 200

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@personal_bp.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    try:

        user = get_user_by_id(user_id)

        return jsonify({"ok": True, "user": user}), 200

    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@personal_bp.route("/user_registration", methods=["POST"])
def user_registration():
    try:
        data = request.get_json()
        new_user = create_new_user(data)

        return (
            jsonify(
                {
                    "ok": True,
                    "message": "Usuario creado con éxito",
                    "user": {
                        "id": new_user.id,
                        "name": new_user.name,
                        "email": new_user.email,
                        "username": new_user.username,
                        "document_id": new_user.document_id,
                        "role_id": new_user.role_id,
                        "branch_id": new_user.branch_id,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@personal_bp.route("/user/<document_id>", methods=["DELETE"])
def delete_user(document_id):
    try:
        eliminate_flag = request.args.get("eliminate", "false").lower() == "true"

        if not eliminate_flag:
            return jsonify({"ok": False, "error": "No se indicó eliminar"}), 400

        success = soft_delete_user_if_requested(document_id)
        if not success:
            return jsonify({"ok": False, "error": "Usuario no encontrado"}), 404

        return (
            jsonify(
                {
                    "ok": True,
                    "message": "Usuario eliminado correctamente",
                    "document_id": document_id,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@personal_bp.route("/user/<document_id>", methods=["PUT"])
def update_user(document_id):
    try:
        data = request.get_json() or {}
        result = update_user_service(document_id, data)
        return jsonify(result), result.get("status", 200)
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

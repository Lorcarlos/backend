from flask import Blueprint, request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from ...services.log.log_service import LogService
from ...models.staff.staff_peticion import AppUser
from ...services.staff.staff import (
    get_user_by_id,
    create_new_user,
    soft_delete_user_if_requested,
    update_user_service,
    serialize_user,
)
from utils.decorators import role_required, jwt_required_custom


personal_bp = Blueprint("personal_bp", __name__)

@personal_bp.route("/users", methods=["GET"])
@personal_bp.route("/users/", methods=["GET"])
@role_required([1])
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
        LogService.create_log(
            {
                "module": f"{__name__}.{get_all_users.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"ok": False, "error": str(e)}), 500


@personal_bp.route("/user/me", methods=["GET"])
@jwt_required_custom
def get_current_user():
    try:
        # Obtener el user_id del JWT
        claims = get_jwt()
        user_id = claims.get("user_id")

        if not user_id:
            return jsonify({"ok": False, "error": "No se pudo identificar al usuario"}), 401

        # Obtener el usuario
        user = get_user_by_id(user_id)

        # Serializar el usuario
        user_data = serialize_user(user)

        return jsonify({"ok": True, "user": user_data}), 200

    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{get_current_user.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"ok": False, "error": str(e)}), 500


@personal_bp.route("/users/<user_id>", methods=["GET"])
@role_required([1])
def get_user(user_id):
    try:

        user = get_user_by_id(user_id)

        return jsonify({"ok": True, "user": user}), 200

    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{get_user.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"ok": False, "error": str(e)}), 500


@personal_bp.route("/user_registration", methods=["POST"])
@role_required([1])
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

    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400

    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{user_registration.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"ok": False, "error": str(e)}), 500


@personal_bp.route("/user/<document_id>", methods=["DELETE"])
@role_required([1])
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
        LogService.create_log(
            {
                "module": f"{__name__}.{delete_user.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"ok": False, "error": str(e)}), 500


@personal_bp.route("/user/<document_id>", methods=["PUT"])
@jwt_required_custom
def update_user(document_id):
    try:
        data = request.get_json() or {}
        result = update_user_service(document_id, data)
        status_code = result.pop("status", 200)
        return jsonify(result), status_code
    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{update_user.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"ok": False, "error": str(e)}), 500
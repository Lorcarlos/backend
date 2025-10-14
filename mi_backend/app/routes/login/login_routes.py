from flask import Blueprint, request
from ...services.log.log_service import LogService
from ...services.login.login_service import login, verify_otp, forgot_password
from flask import jsonify

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["POST"])
def login_route():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        login(username, password)

        return (
            jsonify(
                {
                    "ok": True,
                    "message": "Correo enviado exitosamente",
                }
            ),
            200,
        )

    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{login_route.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp_login():

    try:

        data = request.get_json()

        result = verify_otp(data["username"], data["token"])

        return jsonify(
            {
                "ok": True,
                "access_token": result["access_token"],
                "message": "Inicio de sesión exitoso",
                "username": result["username"],
                "name": result["name"],
                "role": result["role"],
                "branch_id": result["branch_id"],
            },
            200,
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{verify_otp_login.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():

    try:
        data = request.get_json()

        forgot_password(data.get("email"))
        return (
            jsonify(
                {"message": "Si existe el usuario, se enviará el token a tu correo"}
            ),
            200,
        )

    except ValueError as e:
        if e.message == "No se encontró el usuario buscado por email":
            return (
                jsonify(
                    {"message": "Si existe el usuario, se enviará el token a tu correo"}
                ),
                200,
            )
        return (
            jsonify(
                {"error": str(e)}
            ),
            404,
        )

    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{forgot_password.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"error": str(e)}), 500

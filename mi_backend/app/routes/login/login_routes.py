from flask import Blueprint, request
from ...services.log.log_service import LogService
from ...services.login.login_service import (
    login,
    verify_otp,
    forgot_password_service,
    verify_reset_password_otp_service,
    reset_password_service,
    resend_otp_login_service,
    resend_otp_password_service,
)
from flask import jsonify

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["POST"])
def login_route():
    try:
        data = request.get_json()

        login(data)

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

        result = verify_otp(data)

        return (
            jsonify(
                {
                    "ok": True,
                    "access_token": result["access_token"],
                    "message": "Inicio de sesión exitoso",
                    "username": result["username"],
                    "user_id": result["user_id"],
                    "name": result["name"],
                    "role": result["role"],
                    "branch_id": result["branch_id"],
                },
            ),
            200,
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

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

        forgot_password_service(data)

        return (
            jsonify(
                {"message": "Si existe el usuario, se enviará el token a tu correo"}
            ),
            200,
        )

    except ValueError as e:
        if str(e) == "El email ingresado no existe":
            return (
                jsonify(
                    {"message": "Si existe el usuario, se enviará el token a tu correo"}
                ),
                200,
            )
        return (
            jsonify({"error": str(e)}),
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


@auth_bp.route("/verify-otp-password", methods=["POST"])
def verify_otp_reset_password():
    try:

        data = request.get_json()

        result = verify_reset_password_otp_service(data)

        return jsonify({"ok": True, "message": result}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{verify_otp_reset_password.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():

    try:

        data = request.get_json()

        result = reset_password_service(data)

        return jsonify({"ok": True, "message": result}), 200

    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400

    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{reset_password.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/resend-otp-login", methods=["POST"])
def resend_otp_login():
    """
    Endpoint para reenviar el código OTP de login.
    """
    try:
        data = request.get_json()

        result = resend_otp_login_service(data)

        return (
            jsonify(
                {
                    "ok": True,
                    "message": result,
                }
            ),
            200,
        )

    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{resend_otp_login.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/resend-otp-password", methods=["POST"])
def resend_otp_password():
    """
    Endpoint para reenviar el código OTP de recuperación de contraseña.
    """
    try:
        data = request.get_json()

        result = resend_otp_password_service(data)

        return (
            jsonify(
                {
                    "ok": True,
                    "message": result,
                }
            ),
            200,
        )

    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{resend_otp_password.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"error": str(e)}), 500

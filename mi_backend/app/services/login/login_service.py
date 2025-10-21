from ...database import db
from ...models.staff.staff_peticion import AppUser
from ...services.token.token_service import TokenService
from ...services.log.log_service import LogService
from ...services.login_logs.user_logins_service import UserLoginsService
from ...services.staff.staff import get_user_by_email
from ...utils.mail_sender import send_otp_mail
from ...utils.tokenType import TokenType
from ...utils.tokenGenerator import uniqueTokenGenerator
from ...utils.validator import validate_data, validate_email, hash_password
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from flask import jsonify


def login(data):

    required_fields = {"username": str, "password": str}

    validate_data(data, required_fields)

    user = (
        AppUser.query.filter_by(username=data.get("username"))
        .filter(AppUser.deleted_at.is_(None))
        .first()
    )

    if not user:
        raise ValueError("Credenciales inválidas")

    if not check_password_hash(user.hashed_password, data.get("password")):
        raise ValueError("Credenciales inválidas")

    token = uniqueTokenGenerator()

    TokenService.create(
        {"app_user_id": user.id, "token": token, "type": TokenType.OTP_LOGIN.value}
    )

    send_otp_mail(
        f"Código de autenticación {token}",
        user.email,
        f"Tu código de verificación para iniciar sesión es {token}, recuerda que tienes 10 minutos antes de que expire",
    )


def verify_otp(data):

    required_fields = {"username": str, "token": str}

    validate_data(data, required_fields)

    user = (
        AppUser.query.filter_by(username=data["username"])
        .filter(AppUser.deleted_at.is_(None))
        .first()
    )

    if user is None:
        LogService.create_log(
            {
                "module": f"{__name__}.{verify_otp.__name__}",
                "message": "Se ingresó un usuario inválido en el inicio de sesión con otp",
            }
        )
        raise ValueError("El usuario ingresado no existe")

    tokenFound = TokenService.findValidToken(user.id, data["token"])

    if tokenFound is None:
        LogService.create_log(
            {
                "module": f"{__name__}.{verify_otp.__name__}",
                "message": "Se ingresó un token inválido en el inicio de sesión con otp",
            }
        )
        raise ValueError("El token ingresado no existe")

    tokenFound.is_used = True
    db.session.commit()

    # El identity debe ser una cadena (user_id), los datos adicionales van en additional_claims
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "username": user.username,
            "role": user.role_id,
            "user_id": user.id,
            "is_active": user.is_active
        }
    )

    UserLoginsService.create(user.id)

    return {
        "access_token": access_token,
        "message": "Inicio de sesión exitoso",
        "username": user.username,
        "name": user.name,
        "role": user.role_id,
        "branch_id": user.branch_id,
        "user_id": user.id,
    }


def forgot_password_service(data):

    required_fields = {"email": str}

    validate_data(data, required_fields)

    email = data.get("email")

    validate_email(email)

    user = get_user_by_email(email)

    if user is None:
        LogService.create_log(
            {
                "module": f"{__name__}.{forgot_password_service.__name__}",
                "message": "Se ingresó un email inválido en la petición de token para reseteo de contraseña",
            }
        )
        raise ValueError("El email ingresado no existe")

    token = uniqueTokenGenerator()

    TokenService.create(
        {"token": token, "app_user_id": user.id, "type": TokenType.RESET_PASSWORD.value}
    )

    send_otp_mail(
        f"Código para reestablecer contraseña {token}",
        user.email,
        f"Hola! aquí tienes tu código para reestablecer la contraseña de tu usuario: {token}. Si no solicitaste esto, por favor contacta con soporte inmediatamente.",
    )


def verify_reset_password_otp_service(data):

    required_fields = {"email": str, "token": str}

    validate_data(data, required_fields)

    user = get_user_by_email(data["email"])

    if user is None:
        LogService.create_log(
            {
                "module": f"{__name__}.{verify_reset_password_otp_service.__name__}",
                "message": "Se ingresó un email inválido en el reseteo de contraseña con otp",
            }
        )
        raise ValueError("El email ingresado no existe")

    tokenFound = TokenService.findValidToken(user.id, data["token"])

    if tokenFound is None:
        LogService.create_log(
            {
                "module": f"{__name__}.{verify_reset_password_otp_service.__name__}",
                "message": "Se ingresó un token inválido en el reseteo de contraseña con otp",
            }
        )
        raise ValueError("El token ingresado no existe")

    tokenFound.is_used = True
    db.session.commit()

    return "Se ingresó el token correctamente"


def reset_password_service(data):

    required_fields = {
        "email": str,
        "new_password": str,
        "confirm_password": str,
    }

    validate_data(data, required_fields)

    new_password = data["new_password"]

    if new_password != data["confirm_password"]:
        LogService.create_log(
            {
                "module": f"{__name__}.{reset_password_service.__name__}",
                "message": "La nueva contraseña y el repetir contraseña no coinciden",
            }
        )
        raise ValueError("Las contraseñas ingresadas no coinciden")

    user = get_user_by_email(data["email"])

    if user is None:
        LogService.create_log(
            {
                "module": f"{__name__}.{reset_password_service.__name__}",
                "message": "Se ingresó un email inválido en el reseteo de contraseña",
            }
        )
        raise ValueError("El email ingresado no existe")

    new_hashed_password = hash_password(new_password)

    user.hashed_password = new_hashed_password

    db.session.commit()

    return "Contraseña restaurada exitosamente"

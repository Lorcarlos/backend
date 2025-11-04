from ...database import db
from ...models.staff.staff_peticion import AppUser
from ...models.rate_limit.rate_limit import RateLimit
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
import time
import random


def login(data):

    required_fields = {"username": str, "password": str}

    validate_data(data, required_fields)

    username = data.get("username")

    # Check if user is blocked
    if RateLimit.is_blocked(username, "login"):
        remaining_time = RateLimit.get_block_time_remaining(username, "login")
        LogService.create_log(
            {
                "module": f"{__name__}.{login.__name__}",
                "message": f"Intento de login bloqueado para usuario: {username}",
            }
        )
        raise ValueError(f"Cuenta bloqueada temporalmente. Intenta nuevamente en {remaining_time} minutos")

    user = (
        AppUser.query.filter_by(username=username)
        .filter(AppUser.deleted_at.is_(None))
        .first()
    )

    if not user:
        # Record failed attempt
        remaining, is_blocked, block_until = RateLimit.record_attempt(username, "login", max_attempts=5, block_duration_minutes=30)
        LogService.create_log(
            {
                "module": f"{__name__}.{login.__name__}",
                "message": f"Intento de login fallido - usuario no existe: {username}. Intentos restantes: {remaining}",
            }
        )
        if is_blocked:
            raise ValueError("Demasiados intentos fallidos. Cuenta bloqueada por 30 minutos")
        if remaining > 0:
            raise ValueError(f"Credenciales invalidas. Le quedan {remaining} intentos")
        raise ValueError("Credenciales invalidas")

    if not check_password_hash(user.hashed_password, data.get("password")):
        # Record failed attempt
        remaining, is_blocked, block_until = RateLimit.record_attempt(username, "login", max_attempts=5, block_duration_minutes=30)
        LogService.create_log(
            {
                "module": f"{__name__}.{login.__name__}",
                "message": f"Intento de login fallido - contraseña incorrecta para: {username}. Intentos restantes: {remaining}",
            }
        )
        if is_blocked:
            raise ValueError("Demasiados intentos fallidos. Cuenta bloqueada por 30 minutos")
        if remaining > 0:
            raise ValueError(f"Credenciales invalidas. Le quedan {remaining} intentos")
        raise ValueError("Credenciales invalidas")

    # Reset attempts on successful login
    RateLimit.reset_attempts(username, "login")

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

    username = data["username"]

    # Check if user is blocked for OTP verification
    if RateLimit.is_blocked(username, "verify-otp"):
        remaining_time = RateLimit.get_block_time_remaining(username, "verify-otp")
        LogService.create_log(
            {
                "module": f"{__name__}.{verify_otp.__name__}",
                "message": f"Intento de verificación OTP bloqueado para usuario: {username}",
            }
        )
        raise ValueError(f"Cuenta bloqueada temporalmente. Intenta nuevamente en {remaining_time} minutos")

    user = (
        AppUser.query.filter_by(username=username)
        .filter(AppUser.deleted_at.is_(None))
        .first()
    )

    if user is None:
        # Record failed attempt
        remaining, is_blocked, block_until = RateLimit.record_attempt(username, "verify-otp", max_attempts=3, block_duration_minutes=15)
        LogService.create_log(
            {
                "module": f"{__name__}.{verify_otp.__name__}",
                "message": f"Intento de verificación OTP fallido - usuario no existe: {username}. Intentos restantes: {remaining}",
            }
        )
        if is_blocked:
            raise ValueError("Demasiados intentos fallidos. Cuenta bloqueada por 15 minutos")
        if remaining > 0:
            raise ValueError(f"El usuario ingresado no existe. Le quedan {remaining} intentos")
        raise ValueError("El usuario ingresado no existe")

    try:
        tokenFound = TokenService.findValidToken(user.id, data["token"])
    except ValueError:
        # Token is invalid - record failed attempt
        remaining, is_blocked, block_until = RateLimit.record_attempt(username, "verify-otp", max_attempts=3, block_duration_minutes=15)
        LogService.create_log(
            {
                "module": f"{__name__}.{verify_otp.__name__}",
                "message": f"Intento de verificación OTP fallido - token inválido para: {username}. Intentos restantes: {remaining}",
            }
        )
        if is_blocked:
            raise ValueError("Demasiados intentos fallidos. Cuenta bloqueada por 15 minutos")
        if remaining > 0:
            raise ValueError(f"El token ingresado no existe. Le quedan {remaining} intentos")
        raise ValueError("El token ingresado no existe")

    # Reset attempts on successful OTP verification
    RateLimit.reset_attempts(username, "verify-otp")

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
        # Agregar un delay aleatorio (1.5 a 3 segundos) para prevenir timing attacks
        # Esto hace que el tiempo de respuesta sea similar al envío de un email
        time.sleep(random.uniform(1.5, 3.0))

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

    email = data["email"]

    # Check if email is blocked for password reset OTP verification
    if RateLimit.is_blocked(email, "verify-otp-password"):
        remaining_time = RateLimit.get_block_time_remaining(email, "verify-otp-password")
        LogService.create_log(
            {
                "module": f"{__name__}.{verify_reset_password_otp_service.__name__}",
                "message": f"Intento de verificación OTP de reseteo bloqueado para email: {email}",
            }
        )
        raise ValueError(f"Cuenta bloqueada temporalmente. Intenta nuevamente en {remaining_time} minutos")

    user = get_user_by_email(email)

    if user is None:
        # Record failed attempt
        remaining, is_blocked, block_until = RateLimit.record_attempt(email, "verify-otp-password", max_attempts=3, block_duration_minutes=15)
        LogService.create_log(
            {
                "module": f"{__name__}.{verify_reset_password_otp_service.__name__}",
                "message": f"Intento de verificación OTP de reseteo fallido - email no existe: {email}. Intentos restantes: {remaining}",
            }
        )
        if is_blocked:
            raise ValueError("Demasiados intentos fallidos. Cuenta bloqueada por 15 minutos")
        if remaining > 0:
            raise ValueError(f"El email ingresado no existe. Le quedan {remaining} intentos")
        raise ValueError("El email ingresado no existe")

    try:
        tokenFound = TokenService.findValidToken(user.id, data["token"])
    except ValueError:
        # Token is invalid - record failed attempt
        remaining, is_blocked, block_until = RateLimit.record_attempt(email, "verify-otp-password", max_attempts=3, block_duration_minutes=15)
        LogService.create_log(
            {
                "module": f"{__name__}.{verify_reset_password_otp_service.__name__}",
                "message": f"Intento de verificación OTP de reseteo fallido - token inválido para: {email}. Intentos restantes: {remaining}",
            }
        )
        if is_blocked:
            raise ValueError("Demasiados intentos fallidos. Cuenta bloqueada por 15 minutos")
        if remaining > 0:
            raise ValueError(f"El token ingresado no existe. Le quedan {remaining} intentos")
        raise ValueError("El token ingresado no existe")

    # Reset attempts on successful password reset OTP verification
    RateLimit.reset_attempts(email, "verify-otp-password")

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


def resend_otp_login_service(data):
    """
    Reenvía el código OTP para login.
    Genera un nuevo código y lo envía al correo del usuario.
    """
    required_fields = {"username": str}

    validate_data(data, required_fields)

    username = data.get("username")

    # Check if user is blocked
    if RateLimit.is_blocked(username, "login"):
        remaining_time = RateLimit.get_block_time_remaining(username, "login")
        LogService.create_log(
            {
                "module": f"{__name__}.{resend_otp_login_service.__name__}",
                "message": f"Intento de reenvío de OTP bloqueado para usuario: {username}",
            }
        )
        raise ValueError(f"Cuenta bloqueada temporalmente. Intenta nuevamente en {remaining_time} minutos")

    user = (
        AppUser.query.filter_by(username=username)
        .filter(AppUser.deleted_at.is_(None))
        .first()
    )

    if not user:
        LogService.create_log(
            {
                "module": f"{__name__}.{resend_otp_login_service.__name__}",
                "message": f"Intento de reenvío de OTP - usuario no existe: {username}",
            }
        )
        raise ValueError("El usuario ingresado no existe")

    # Generar nuevo token
    token = uniqueTokenGenerator()

    # Crear nuevo token en la base de datos
    TokenService.create(
        {"app_user_id": user.id, "token": token, "type": TokenType.OTP_LOGIN.value}
    )

    # Enviar correo con el nuevo código
    send_otp_mail(
        f"Código de autenticación {token}",
        user.email,
        f"Tu código de verificación para iniciar sesión es {token}, recuerda que tienes 10 minutos antes de que expire",
    )

    LogService.create_log(
        {
            "module": f"{__name__}.{resend_otp_login_service.__name__}",
            "message": f"OTP reenviado exitosamente para usuario: {username}",
        }
    )

    return "Código OTP reenviado exitosamente"


def resend_otp_password_service(data):
    """
    Reenvía el código OTP para recuperación de contraseña.
    Genera un nuevo código y lo envía al correo del usuario.
    """
    required_fields = {"email": str}

    validate_data(data, required_fields)

    email = data.get("email")

    validate_email(email)

    user = get_user_by_email(email)

    if user is None:
        # Agregar un delay aleatorio para prevenir timing attacks
        time.sleep(random.uniform(1.5, 3.0))

        LogService.create_log(
            {
                "module": f"{__name__}.{resend_otp_password_service.__name__}",
                "message": "Se ingresó un email inválido en el reenvío de token para reseteo de contraseña",
            }
        )
        raise ValueError("El email ingresado no existe")

    # Generar nuevo token
    token = uniqueTokenGenerator()

    # Crear nuevo token en la base de datos
    TokenService.create(
        {"token": token, "app_user_id": user.id, "type": TokenType.RESET_PASSWORD.value}
    )

    # Enviar correo con el nuevo código
    send_otp_mail(
        f"Código para reestablecer contraseña {token}",
        user.email,
        f"Hola! aquí tienes tu código para reestablecer la contraseña de tu usuario: {token}. Si no solicitaste esto, por favor contacta con soporte inmediatamente.",
    )

    LogService.create_log(
        {
            "module": f"{__name__}.{resend_otp_password_service.__name__}",
            "message": f"Token de reseteo de contraseña reenviado exitosamente para email: {email}",
        }
    )

    return "Código OTP reenviado exitosamente"

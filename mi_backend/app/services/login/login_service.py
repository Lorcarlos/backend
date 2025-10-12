from ...database import db
from ...models.staff.staff_peticion import AppUser
from ...services.token.token_service import TokenService
from ...services.login_logs.user_logins_service import UserLoginsService
from ...utils.mail_sender import send_otp_mail
from ...utils.tokenType import TokenType
from ...utils.tokenGenerator import uniqueTokenGenerator
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from flask import jsonify


def login(username, password):

    user = (
        AppUser.query.filter_by(username=username)
        .filter(AppUser.deleted_at.is_(None))
        .first()
    )

    if not user:
        raise ValueError("Credenciales inválidas")


    if not check_password_hash(user.hashed_password, password):
        raise ValueError("Credenciales inválidas")

    tokenSet = {t.token for t in TokenService.getAllTokens()}

    token = uniqueTokenGenerator(tokenSet)

    TokenService.create(
        {"app_user_id": user.id, "token": token, "type": TokenType.OTP_LOGIN.value}
    )

    send_otp_mail(
        f"Código de autenticación {token}",
        user.email,
        f"Tu código de verificación para iniciar sesión es {token}, recuerda que tienes 10 minutos antes de que expire",
    )


def verify_otp(username, token):

    user = (
        AppUser.query.filter_by(username=username)
        .filter(AppUser.deleted_at.is_(None))
        .first()
    )

    tokenFound = TokenService.findValidToken(user.id, token)

    tokenFound.is_used = True
    db.session.commit()

    access_token = create_access_token(
        identity={"username": user.username, "role": user.role_id}
    )

    # CREAR ENTIDAD LOGIN EN LA BD Y CREAR LOG DE INICIO DE SESIÓN
    UserLoginsService.create(user.id)

    return {
        "access_token": access_token,
        "message": "Inicio de sesión exitoso",
        "username": user.username,
        "role": user.role_id,
        "branch_id": user.branch_id,
    }

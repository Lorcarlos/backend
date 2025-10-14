from ...models.token.token import Token
from ...database import db
from ...services.log.log_service import LogService
from datetime import datetime, timedelta, timezone


class TokenService:

    @staticmethod
    def getAllTokens():
        return Token.query.all()

    @staticmethod
    def create(token):

        new_token = Token(
            token=token["token"],
            app_user_id=token["app_user_id"],
            type=token["type"],
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
        )

        db.session.add(new_token)
        db.session.commit()

        return new_token

    @staticmethod
    def findValidToken(app_user_id, token):

        token = Token.query.filter(
            Token.app_user_id == app_user_id,
            Token.token == token,
            Token.expires_at > datetime.now(timezone.utc),
            Token.is_used == False,
        ).first()

        if token is None:
            LogService.create_log(
                {
                    "module": f"{TokenService.__name__}.{TokenService.findValidToken.__name__}",
                    "message": "Se ingresó un token inválido",
                }
            )
            raise ValueError("El token buscado es inválido")

        return token

from ...models.login_logs.user_logins import UserLogins
from ...database import db


class UserLoginsService:

    def get_all_users_logins():

        users_logins = UserLogins.query.all()

        return [u_logins.to_dict() for u_logins in users_logins]

    def find_user_logins_by_user_id(app_user_id):

        user_logins = UserLogins.query.filter(
            UserLogins.app_user_id == app_user_id
        ).first()

        if user_logins is None:
            raise ValueError("El usuario buscado no tiene logins asociados")

        return user_logins.to_dict()

    def create(app_user_id):

        new_user_login = UserLogins(app_user_id=app_user_id)

        db.session.add(new_user_login)

        db.session.commit()

from ...models.log.log import Log
from ...database import db


class LogService:

    def get_all_logs():

        logs = Log.query.all()

        return [log.to_dict() for log in logs]

    def get_log_by_id(id_log):

        log = Log.query.filter(Log.id == id_log).first()

        if log is None:
            LogService.create_log(
                {
                    "module": f"{LogService.__name__}.{LogService.get_log_by_id.__name__}",
                    "message": "No se encontró el log buscado por id",
                }
            )
            raise ValueError("No se encontró el log")

        return log.to_dict()

    def create_log(log):

        new_log = Log(module=log["module"], message=log["message"])

        db.session.add(new_log)
        db.session.commit()

        return new_log

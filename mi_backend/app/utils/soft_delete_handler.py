from ..services.log.log_service import LogService

class SoftDeleteHandler:

    @staticmethod
    def create_or_restore(model, unique_filters, data, restore_fn, create_fn):
        """
        model: clase SQLAlchemy (ej. AppUser, Product, Supplier)
        unique_condition: condición SQLAlchemy (puede ser and_(...) o or_(...))
        data: datos del nuevo registro
        restore_fn: función para restaurar
        create_fn: función para crear
        """

        # Verificar si existe ACTIVO (no eliminado)
        existing_active = model.query.filter(
            unique_filters, model.deleted_at.is_(None)
        ).first()

        if existing_active:
            LogService.create_log(
                {
                    "module": f"{SoftDeleteHandler.__name__}.{SoftDeleteHandler.create_or_restore.__name__}",
                    "message": f"Se intentó crear el modelo {model.__name__}, el cual ya existe en el sistema",
                }
            )
            raise ValueError(f"El {model.__name__} ya existe en el sistema")

        # Verificar si existe eliminado
        existing_deleted = model.query.filter(
            unique_filters, model.deleted_at.isnot(None)
        ).first()

        if existing_deleted:
            return restore_fn(existing_deleted, data)

        # Crear nuevo
        return create_fn(data)

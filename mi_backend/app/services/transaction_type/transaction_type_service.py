from ...models.transaction_type.transaction_type import TransactionType
from ...services.log.log_service import LogService


class TransactionTypeService:

    @staticmethod
    def get_all_transaction_types() -> list[dict]:

        transaction_types = TransactionType.query.filter(
            TransactionType.deleted_at.is_(None)
        ).all()

        return [transaction_type.to_dict() for transaction_type in transaction_types]

    @staticmethod
    def get_transaction_type_by_id(id_transaction_type):

        transaction_type = TransactionType.query.filter(
            TransactionType.deleted_at.is_(None),
            TransactionType.id == id_transaction_type,
        ).first()

        if transaction_type is None:
            LogService.create_log(
                {
                    "module": f"{TransactionTypeService.__name__}.{TransactionTypeService.get_transaction_type_by_id.__name__}",
                    "message": "No se encontró el tipo de transacción buscado por id",
                }
            )
            raise ValueError("Tipo de transacción no encontrado")

        return transaction_type.to_dict()

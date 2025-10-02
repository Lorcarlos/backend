from ...models.transaction_type.transaction_type import TransactionType


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
            raise ValueError("Tipo de transacción no encontrado")

        return transaction_type.to_dict()

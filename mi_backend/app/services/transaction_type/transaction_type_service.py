from ...models.transaction.transaction_type import Transaction_type


class Transaction_type_service:

    @staticmethod
    def get_all_transaction_types() -> list[dict]:

        transaction_types = Transaction_type.query.filter(
            Transaction_type.deleted_at.is_(None)
        ).all()

        return [transaction_type.to_dict() for transaction_type in transaction_types]

    @staticmethod
    def get_transaction_type_by_id(id_transaction_type):

        transaction_type = Transaction_type.query.filter(
            Transaction_type.deleted_at.is_(None),
            Transaction_type.id == id_transaction_type,
        ).first()

        if transaction_type is None:
            raise ValueError("Tipo de transacción no encontrado")

        return transaction_type.to_dict()

from ...models.product_transaction.product_transaction import ProductTransaction
from ...services.transaction_type.transaction_type_service import TransactionTypeService
from ...services.inventory.inventory_service import InventoryService
from ...services.branch.branch_service import BranchService
from ...services.product.product_service import ProductService
from ...services.supplier.supplier_service import SupplierService
from ...services.staff.staff import get_user_by_id
from ...database import db
from ...utils.validator import validate_data
from ...utils.date_conversor import parse_transaction_date
from decimal import Decimal


class ProductTransactionService:

    @staticmethod
    def get_all_products_transactions():

        product_transactions = ProductTransaction.query.all()

        return [p_transaction.to_dict() for p_transaction in product_transactions]

    @staticmethod
    def get_product_transaction_by_id(id_product_transaction):

        product_transaction = ProductTransaction.query.filter(
            ProductTransaction.id == id_product_transaction
        ).first()

        if product_transaction is None:
            raise ValueError("Transacción no encontrada")

        return product_transaction.to_dict()

    @staticmethod
    def create_product_transaction_service(product_transaction):

        required_fields = {
            "description": str,
            "quantity": int,
            "unit_price": (int, float),
            "transaction_date": str,
            "product_id": (int, str),
            "branch_id": (int, str),
            "transaction_type_id": (int, str),
            "app_user_id": (int, str),
        }

        validate_data(product_transaction, required_fields)

        ProductTransactionService.validate_product_transaction_data(product_transaction)

        unit_price = Decimal(product_transaction["unit_price"])
        total_price = unit_price * product_transaction["quantity"]

        # Validar y parsear la fecha con formatos estrictos
        parsed_date = parse_transaction_date(product_transaction["transaction_date"])

        transaction_type = TransactionTypeService.get_transaction_type_by_id(
            product_transaction["transaction_type_id"]
        )

        try:

            InventoryService.update_inventory(product_transaction, transaction_type)

            # Crear la transacción de producto
            new_product_transaction = ProductTransaction(
                description=product_transaction["description"],
                quantity=product_transaction["quantity"],
                unit_price=unit_price,
                total_price=total_price,
                transaction_date=parsed_date,
                product_id=product_transaction["product_id"],
                supplier_id=product_transaction.get("supplier_id"),  # Opcional
                branch_id=product_transaction["branch_id"],
                transaction_type_id=product_transaction["transaction_type_id"],
                app_user_id=product_transaction["app_user_id"],
            )

            db.session.add(new_product_transaction)
            db.session.commit()

            return new_product_transaction

        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def validate_product_transaction_data(product_transaction):

        ProductService.get_product_by_id(product_transaction["product_id"])

        BranchService.get_branch_by_id(product_transaction["branch_id"])

        get_user_by_id(product_transaction["app_user_id"]) # Validamos si el usuario de la transacción existe

        if "supplier_id" in product_transaction and product_transaction["supplier_id"]:
            SupplierService.get_supplier_by_id(product_transaction["supplier_id"])

        if product_transaction["quantity"] < 0:
            raise ValueError("La Cantidad no puede ser negativa")

        if len(product_transaction["description"].strip()) < 5:
            raise ValueError("La descripción debe ser mayor a 5 caracteres")

        if product_transaction["unit_price"] < 0:
            raise ValueError(f"El precio unitario no puede ser negativo")

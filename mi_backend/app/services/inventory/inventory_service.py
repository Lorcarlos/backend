from ...models.inventory.inventory import Inventory
from ...database import db


class InventoryService:

    @staticmethod
    def _create_inventory(inventory):

        inventoryExists = InventoryService.get_inventory_by_product_and_branch(
            inventory["product_id"], inventory["branch_id"]
        )

        if inventoryExists:
            raise ValueError(
                f"El inventario para el producto con ID {inventory['product_id']} en la sede con ID {inventory['branch_id']} ya existe."
            )

        new_inventory = Inventory(
            product_id=inventory["product_id"],
            branch_id=inventory["branch_id"],
            quantity=0,
        )

        db.session.add(new_inventory)

        return new_inventory

    @staticmethod
    def get_all_inventories(branch_id=None, product_id=None):
        query = Inventory.query.filter(Inventory.deleted_at.is_(None))

        if branch_id:
            query = query.filter(Inventory.branch_id == branch_id)

        if product_id:
            query = query.filter(Inventory.product_id == product_id)

        inventories = query.all()
        return [inventory.to_dict() for inventory in inventories]

    @staticmethod
    def get_inventory_by_id(id_inventory):
        inventory = Inventory.query.filter(
            Inventory.deleted_at.is_(None), Inventory.id == id_inventory
        ).first()

        if inventory is None:
            raise ValueError("No se encontró el inventario")

        return inventory.to_dict()

    @staticmethod
    def get_inventory_by_product_and_branch(id_product, id_branch):

        inventory = Inventory.query.filter(
            Inventory.deleted_at.is_(None),
            Inventory.product_id == id_product,
            Inventory.branch_id == id_branch,
        ).first()

        return inventory

    @staticmethod
    def update_inventory(product_transaction, transaction_type):

        inventory = InventoryService.get_inventory_by_product_and_branch(
            product_transaction["product_id"], product_transaction["branch_id"]
        )

        if not inventory:
            if (
                transaction_type["direction"] == "IN"
                or transaction_type["name"] == "ajuste positivo"
            ):
                inventory = InventoryService._create_inventory(
                    {
                        "product_id": product_transaction["product_id"],
                        "branch_id": product_transaction["branch_id"],
                    }
                )
            else:
                raise ValueError("No existe inventario para este producto en esta sede")

        inventory.quantity = InventoryService.adjust_quantity(
            transaction_type, product_transaction, inventory.quantity
        )

        db.session.add(inventory)

    @staticmethod
    def adjust_quantity(transaction_type, product_transaction, quantity):
        if (
            transaction_type["direction"] == "OUT"
            or transaction_type["name"] == "ajuste negativo"
        ):
            if quantity < product_transaction["quantity"]:
                raise ValueError("No hay suficiente stock en el inventario")
            quantity -= product_transaction["quantity"]

        elif (
            transaction_type["direction"] == "IN"
            or transaction_type["name"] == "ajuste positivo"
        ):
            quantity += product_transaction["quantity"]

        return quantity

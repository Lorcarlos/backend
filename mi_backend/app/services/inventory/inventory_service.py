from ...models.inventort.inventory import Inventory


class InventoryService:

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

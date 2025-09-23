from ...models.inventory import Inventory


class InventoryService:

    @staticmethod
    def get_all_inventories():

        inventories = Inventory.query.filter(Inventory.deleted_at.is_(None)).all()

        return [inventory.to_dict() for inventory in inventories]

    @staticmethod
    def get_inventory_by_id(id_inventory):

        inventory = Inventory.query.filter(
            Inventory.deleted_at.is_(None), Inventory.id == id_inventory
        ).first()

        if inventory is None:
            raise ValueError("No se encontró el inventario")

        return inventory.to_dict()

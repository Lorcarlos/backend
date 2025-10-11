from ...models.inventory.inventory import Inventory
from ...database import db
from sqlalchemy import func


class InventoryService:

    @staticmethod
    def _create_inventory(inventory):
        # ... (código existente) ...
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
        # ... (código existente) ...
        query = Inventory.query.filter(Inventory.deleted_at.is_(None))

        if branch_id:
            query = query.filter(Inventory.branch_id == branch_id)

        if product_id:
            query = query.filter(Inventory.product_id == product_id)

        inventories = query.all()
        return [inventory.to_dict() for inventory in inventories]

    @staticmethod
    def get_inventory_by_product_and_branch(id_product, id_branch):
        # ... (código existente) ...
        inventory = Inventory.query.filter(
            Inventory.deleted_at.is_(None),
            Inventory.product_id == id_product,
            Inventory.branch_id == id_branch,
        ).first()

        return inventory

    @staticmethod
    def update_inventory(product_transaction, transaction_type):
        # ... (código existente) ...
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
        # ... (código existente) ...
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

    @staticmethod
    def get_inventory_by_id(id_inventory):
        # ... (código existente) ...
        inventory = Inventory.query.get(id_inventory)
        if not inventory:
            raise ValueError("Inventario no encontrado")
        return inventory.to_dict()
    
    # --- FUNCIONES DE CÁLCULO DE PORCENTAJE (EXISTENTES Y REUBICADAS) ---

    @staticmethod
    def _calculate_stock_percentage(current_quantity, max_capacity):
        min_max_capacity = max(1, max_capacity)
        
        percentage = min(100, round((current_quantity / min_max_capacity) * 100))
        return percentage

    @staticmethod
    def _get_average_if_low_stock(percentage, current_quantity, threshold=50):
        
        if current_quantity < threshold:
            average_with_warning = (percentage + 10) / 2
            return round(average_with_warning)
        
        return percentage
        
    @staticmethod
    def _get_max_quantity_by_product():
        
        max_quantities = db.session.query(
            Inventory.product_id, 
            func.max(Inventory.quantity).label('max_q')
        ).filter(
            Inventory.deleted_at.is_(None)
        ).group_by(
            Inventory.product_id
        ).all()
        
        max_map = {item.product_id: item.max_q for item in max_quantities}
        
        return max_map

    # --- NUEVAS FUNCIONES DE STOCK LEVEL (REQUERIDAS POR EL FRONTEND) ---
    
    @staticmethod
    def get_all_inventories_with_stock_level(branch_id=None, product_id=None):
        """
        Calcula y añade los campos de nivel de stock a todos los inventarios.
        Esta función es la que llama tu frontend.
        """
        inventories_data = InventoryService.get_all_inventories(branch_id, product_id)
        
        max_quantities_map = InventoryService._get_max_quantity_by_product()

        DEFAULT_MAX_CAPACITY = 100 

        for item in inventories_data:
            current_quantity = item["quantity"]
            product_id = item["product_id"]
            
            max_capacity = max_quantities_map.get(product_id, DEFAULT_MAX_CAPACITY)
            
            # Asegura que la capacidad máxima usada sea al menos la cantidad actual
            max_capacity = max(max_capacity, current_quantity)
            
            percentage = InventoryService._calculate_stock_percentage(
                current_quantity, max_capacity
            )
            item["stock_percentage_real"] = percentage
            item["max_capacity_used"] = max_capacity
            
            item["stock_level_adjusted"] = InventoryService._get_average_if_low_stock(
                percentage, current_quantity
            )
            
        return inventories_data

    # --- FUNCIÓN get_inventory_percentage (TU FUNCIÓN REUBICADA) ---
    
    @staticmethod
    def get_inventory_percentage(branch_id=None, product_id=None):
        """
        Devuelve solo el porcentaje de stock del primer ítem encontrado.
        Llama a get_all_inventories_with_stock_level internamente.
        """
        # Ya que está dentro de la clase, puede llamarse directamente
        inventories_with_levels = InventoryService.get_all_inventories_with_stock_level(branch_id, product_id)

        if inventories_with_levels:
            # Devuelve el porcentaje real del primer ítem encontrado
            return inventories_with_levels[0]["stock_percentage_real"] 
        else:
            return 0
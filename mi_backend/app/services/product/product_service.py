from ...models.product.product import Product
from ...utils.validator import validate_data
from ...utils.soft_delete_handler import SoftDeleteHandler
from ...services.log.log_service import LogService
from ...database import db
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy import and_
from  ...models.inventory.inventory import Inventory


class ProductService:

    @staticmethod
    def get_all_products() -> list[dict]:
        products = Product.query.filter(Product.deleted_at.is_(None)).all()
        return [p.to_dict() for p in products]

    @staticmethod
    def create_product_service(product):
        required_fields = {
            "name": str,
            "size": str,
            "price": (int, float, str),
            "description": str,
        }

        validate_data(product, required_fields)

        product["name"] = product["name"].strip().lower()
        product["size"] = product["size"].strip().lower()
        
        try:
            price = Decimal(str(product["price"]))
        except Exception:
            raise ValueError("El precio debe ser un número válido")

        try:
            quantity = int(product["quantity"])
            if quantity < 0:
                raise ValueError("La cantidad no puede ser negativa")
        except Exception:
            raise ValueError("La cantidad debe ser un número entero válido")
        
        # 3. VERIFICACIÓN DE EXISTENCIA
        product_exists = Product.query.filter(
            Product.deleted_at.is_(None),
            Product.name == product["name"],
            Product.size == product["size"],
        ).first()

        if product_exists:
            raise ValueError("El producto ingresado ya existe")


        # 4. CREAR PRODUCTO
        new_product = Product(
            name=product["name"],
            size=product["size"],
            price=price,
            description=product["description"],
            is_active=product.get("is_active", True),
        )

        db.session.add(new_product)
        db.session.flush() # Obtiene el new_product.id

        # 5. CREAR O ACTUALIZAR INVENTARIO
        # Asumiendo que branch_id siempre es 1 si el frontend no lo envía.
        branch_id = product.get("branch_id", 1) 
        
        # No deberías necesitar buscar, ya que es un producto NUEVO.
        # Solo creamos el nuevo registro de inventario.
        
        new_inventory = Inventory(
            product_id=new_product.id,
            branch_id=branch_id,
            quantity=quantity, # <--- ¡Aquí se guarda la cantidad!
        )
        db.session.add(new_inventory)

        db.session.commit()

        return new_product # Devuelve el producto creado
    @staticmethod
    def delete_product_by_id(id_product):
        product_to_delete = ProductService.get_product_by_id(id_product)
        product_to_delete.deleted_at = datetime.now(timezone.utc)
        db.session.commit()
        return True

    @staticmethod
    def get_product_by_id(id_product):
        product = Product.query.filter(
            Product.deleted_at.is_(None), Product.id == id_product
        ).first()

        if product is None:
            LogService.create_log(
                {
                    "module": f"{ProductService.__name__}.{ProductService.get_product_by_id.__name__}",
                    "message": "No se encontró el producto buscado por id",
                }
            )
            raise ValueError("Producto no encontrado")

        return product

    @staticmethod
    def update_product_by_id(id_product, data):
        product = ProductService.get_product_by_id(id_product)
        allowed_fields = ["name", "size", "price", "description", "is_active"]

        for key, value in data.items():
            if key not in allowed_fields:
                LogService.create_log(
                    {
                        "module": f"{ProductService.__name__}.{ProductService.update_product_by_id.__name__}",
                        "message": f"Se intentó actualizar {key} del producto, lo cuál no está permitido",
                    }
                )
                raise ValueError("Se intentó actualizar un campo inválido")

            if key == "price":
                value = Decimal(value)

            setattr(product, key, value)

        product.name = product.name.strip().lower()
        product.size = product.size.strip().lower()

        if len(product.name) < 3:
            LogService.create_log(
                {
                    "module": f"{ProductService.__name__}.{ProductService.update_product_by_id.__name__}",
                    "message": "Se ingresó un nombre de producto de menos de 3 caracteres",
                }
            )
            raise ValueError("El nombre del producto no puede ser menor a 3 caracteres")

        with db.session.no_autoflush:
            product_exists = Product.query.filter(
                Product.deleted_at.is_(None),
                Product.id != product.id,
                Product.name == product.name,
                Product.size == product.size,
            ).first()

            if product_exists:
                LogService.create_log(
                    {
                        "module": f"{ProductService.__name__}.{ProductService.update_product_by_id.__name__}",
                        "message": "Se intentó actualizar un producto con un nombre y tamaño existente",
                    }
                )
                raise ValueError("Ya existe otro producto con el mismo nombre y tamaño")

        db.session.commit()

        return product

    @staticmethod
    def restore_deleted_product(existing_product: Product, new_data: dict) -> Product:
        """Restaura producto eliminado actualizando todos los campos pero manteniendo created_at original"""
        # Actualizar todos los campos de datos
        existing_product.name = new_data["name"].strip().lower()
        existing_product.size = new_data["size"].strip().lower()
        existing_product.price = Decimal(new_data["price"])
        existing_product.description = new_data["description"]
        existing_product.is_active = new_data.get("is_active", True)

        # Solo actualizar updated_at y limpiar deleted_at
        existing_product.updated_at = datetime.now(timezone.utc)
        existing_product.deleted_at = None
        # created_at se mantiene igual (cuándo se creó originalmente)

        db.session.commit()
        return existing_product

    @staticmethod
    def create_fresh_product(product_data: dict) -> Product:
        """Crea un producto completamente nuevo"""
        price = Decimal(product_data["price"])

        new_product = Product(
            name=product_data["name"],
            size=product_data["size"],
            price=price,
            description=product_data["description"],
            is_active=product_data.get("is_active", True),
        )

        db.session.add(new_product)
        db.session.commit()

        return new_product

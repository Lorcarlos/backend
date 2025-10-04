from ...models.product.product import Product
from ...utils.validator import validate_data
from ...utils.soft_delete_handler import SoftDeleteHandler
from ...database import db
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy import and_


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
            "price": (int, float),
            "description": str,
        }

        validate_data(product, required_fields)

        product["name"] = product["name"].strip().lower()
        product["size"] = product["size"].strip().lower()

        if len(product["name"]) < 3:
            raise ValueError("El nombre del producto no puede ser menor a 3 caracteres")

        # Llama al handler que verifica si el elemento existe y está activo o si existe y está soft_deleted
        return SoftDeleteHandler.create_or_restore(
            model=Product,
            unique_filters=and_(
                Product.name == product["name"], Product.size == product["size"]
            ),
            data=product,
            restore_fn=ProductService.restore_deleted_product,
            create_fn=ProductService.create_fresh_product,
        )

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
            raise ValueError("Producto no encontrado")

        return product

    @staticmethod
    def update_product_by_id(id_product, data):

        product = ProductService.get_product_by_id(id_product)

        allowed_fields = ["name", "size", "price", "description", "is_active"]

        for key, value in data.items():
            if key not in allowed_fields:
                raise ValueError("Se intentó actualizar un campo inválido")

            if key == "price":
                value = Decimal(value)

            setattr(product, key, value)

        product.name = product.name.strip().lower()
        product.size = product.size.strip().lower()

        if len(product.name) < 3:
            raise ValueError("El nombre del producto no puede ser menor a 3 caracteres")

        with db.session.no_autoflush:
            product_exists = Product.query.filter(
                Product.deleted_at.is_(None),
                Product.id != product.id,
                Product.name == product.name,
                Product.size == product.size,
            ).first()

            if product_exists:
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

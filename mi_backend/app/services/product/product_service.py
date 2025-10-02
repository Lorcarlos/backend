from ...models.product.product import Product
from ...validator.validator import validate_data
from ...database import db
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy.orm import Query

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

        product_exists = Product.query.filter(
            Product.deleted_at.is_(None),
            Product.name == product["name"],
            Product.size == product["size"],
        ).first()

        if product_exists:
            raise ValueError("El producto ingresado ya existe")

        price = Decimal(product["price"])

        new_product = Product(
            name=product["name"],
            size=product["size"],
            price=price,
            description=product["description"],
            is_active=product.get("is_active", True),
        )

        db.session.add(new_product)
        db.session.commit()

        return new_product

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
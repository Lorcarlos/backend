from ...models.product import Product
from ...validator.validator import validate_data
from flask import jsonify, request
from ...database import db
from decimal import Decimal
from datetime import datetime, timezone


class ProductService:

    required_fields = {
        "name": str,
        "size": str,
        "price": str,
        "description": str,
    }

    def get_all_products() -> list[dict]:
        products = Product.query.filter(Product.deleted_at.is_(None)).all()
        return [p.to_dict() for p in products]

    def create_product_service(product):

        validate_data(product, ProductService.required_fields)

        if len(product["name"]) < 3:
            raise ValueError("El nombre del producto no puede ser menor a 3 caracteres")

        price = Decimal(product["price"])

        product_exists = Product.query.filter(
            Product.deleted_at.is_(None),
            Product.name == product["name"],
            Product.size == product["size"],
        ).first()

        if product_exists:
            raise ValueError("El producto ingresado ya existe")

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

    def delete_product_by_id(id_product):

        product_to_delete = Product.query.filter(
            Product.deleted_at.is_(None), Product.id == id_product
        ).one_or_none()

        if product_to_delete is None:
            raise ValueError("Producto no encontrado")

        product_to_delete.deleted_at = datetime.now(timezone.utc)

        db.session.add(product_to_delete)
        db.session.commit()

        return True

    def get_product_by_id(id_product):

        product = Product.query.filter(
            Product.deleted_at.is_(None), Product.id == id_product
        ).one_or_none()

        if product is None:
            raise ValueError("Producto no encontrado")

        return product

    def update_product_by_id(id_product, data):

        product_result = Product.query.filter(
            Product.deleted_at.is_(None), 
            Product.id == id_product
        ).one_or_none()

        if product_result is None:
            raise ValueError("El producto buscado no existe")
        
        allowed_fields = ["name", "size", "price", "description", "is_active"]

        for key, value in data.items():
            if key not in allowed_fields:
                raise ValueError("Se intentó actualizar un campo inválido")
                
            if key == "price":
                value = Decimal(value)
                
            setattr(product_result, key, value)

        if len(product_result.name) < 3:
            raise ValueError("El nombre del producto no puede ser menor a 3 caracteres")

        with db.session.no_autoflush:
            product_exists = Product.query.filter(
                Product.deleted_at.is_(None),
                Product.id != product_result.id,
                Product.name == product_result.name,
                Product.size == product_result.size
            ).first()
            
            if product_exists:
                raise ValueError("Ya existe otro producto con el mismo nombre y tamaño")

        db.session.commit()

        return product_result

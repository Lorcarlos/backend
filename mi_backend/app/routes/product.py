from flask import Blueprint, jsonify, request
from ..database import db
from ..models import Product

product_bp = Blueprint("product", __name__)

@product_bp.route("/", methods=["GET"])
def get_roducts():
    try:
        products = Product.query.filter(
            Product.deleted_at.is_(None)
        ).all()
        products_list = [p.to_dict() for p in products]
        return jsonify({"ok":True, "products": products_list})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

@product_bp.route("/create", methods=["POST"])
def create_products():
    try:
        product = request.json

        if(product.get("name") is None):
            raise ValueError("El nombre del producto no puede ser nulo")
        
        if len(product["name"]) < 3:
            raise ValueError("El nombre del producto no puede ser menor a 3 caracteres")
        
        if product.get("size") is None:
            raise ValueError("El tamaño del producto no puede ser nulo")
        
        product_exists = Product.query.filter(
            Product.deleted_at.is_(None),
            Product.name == product["name"],
            Product.size == product["size"]
        ).first()
        
        if product_exists:
            raise ValueError("El producto ingresado ya existe")            
        
        if product.get("price") is None:
            raise ValueError("El precio del producto no puede ser nulo")
        
        price = float(product["price"])
        
        if product.get("description") is None:
            raise ValueError("La descripción del producto no puede ser nula")
        
        new_product = Product(
            name = product["name"],
            size = product["size"],
            price = price,
            description = product["description"],
            is_active = product.get("is_active", True)
        )
        
        db.session.add(new_product)
        db.session.commit()
        
        return jsonify({"ok": True, "product": new_product.id})
                
    except Exception as e:
        return jsonify({"ok":False, "error": str(e)}), 400

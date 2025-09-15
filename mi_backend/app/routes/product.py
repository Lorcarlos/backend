from flask import Blueprint, jsonify, request
from ..database import db
from datetime import datetime, timezone
from ..models import Product

product_bp = Blueprint("product", __name__)

@product_bp.route("/", methods=["GET"])
def get_roducts():
    
    try:
        products = Product.query.filter(
            Product.deleted_at.is_(None)
        ).all()
        products_list = [p.to_dict() for p in products]
        return jsonify({"ok":True, "products": products_list}), 200
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@product_bp.route("/create", methods=["POST"])
def create_product():
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
        
        return jsonify({"ok": True, "product": new_product.id}), 200
                
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@product_bp.route("/delete/<id_product>", methods = ["DELETE"])
def delete_product(id_product):
    
    try:
        id_product = int(id_product)
        if id_product <=0 :
            return jsonify({"ok": False, "error": "El id ingresado debe ser positivo"}), 400
        
        product_to_delete = Product.query.filter(
            Product.deleted_at.is_(None),
            Product.id == id_product
        ).one_or_none()
        
        if product_to_delete is None:
            return jsonify({"ok": False, "error": "No se encontró el producto"}), 404
        
        product_to_delete.deleted_at = datetime.now(timezone.utc)
            
        db.session.commit()
        
        return jsonify({"ok": True}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"ok": False, "error": str(e)}), 500
    
@product_bp.route("/<id_product>", methods = ["GET"])
def get_product(id_product):
    
    try:
        
        id_product = int(id_product)
        if id_product <=0 :
            return jsonify({"ok": False, "error": "El id ingresado debe ser positivo"}), 400
        
        product = Product.query.filter(
            Product.deleted_at.is_(None),
            Product.id == id_product
        ).one_or_none()
        
        if product is None:
            return jsonify({"ok": False, "error": "El id ingresado no existe"}), 404
        
        return jsonify({"ok": True, "product": product.to_dict()}), 200
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
    
@product_bp.route("/update_product/<id_product>", methods = ["PATCH"])
def update_product(id_product):
    try:
        
        id_product = int(id_product)
        
        if id_product <= 0:
            return jsonify({"ok": False, "error": "El id ingresado debe ser positivo"}), 400
        
        product_result = Product.query.filter(
            Product.deleted_at.is_(None),
            Product.id == id_product
        ).one_or_none()
        
        if product_result is None:
            return jsonify({"ok": False, "error": "El producto buscado no existe"}), 404
        
        allowed_fields = ["name", "size", "price", "description", "is_active"]

        for key, value in request.json.items():
            if key in allowed_fields:
                setattr(product_result, key, value)
            else :
                return jsonify({"ok": False, "error": "Se intentó actualizar un campo inválido"}), 400
                
        db.session.commit()
        
        return jsonify({"ok": True, "product": product_result.to_dict()}), 200
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
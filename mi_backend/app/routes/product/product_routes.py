from flask import Blueprint, jsonify, request
from ...database import db
from ...models.product import Product
from ...services.product.product_service import ProductService

product_bp = Blueprint("products", __name__)


@product_bp.route("/", methods=["GET"])
def get_roducts():
    try:
        products = ProductService.get_all_products()
        return jsonify({"ok": True, "products": products}), 200

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@product_bp.route("/", methods=["POST"])
def create_product():
    try:
        product = request.json
        new_product = ProductService.create_product_service(product)
        return jsonify({"ok": True, "product": new_product.id}), 201
    except (ValueError, TypeError) as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@product_bp.route("/<id_product>", methods=["DELETE"])
def delete_product(id_product):

    try:
        id_product = int(id_product)
        if id_product <= 0:
            return jsonify({"ok": False, "error": "El id ingresado debe ser positivo"}), 400

        ProductService.delete_product_by_id(id_product)

        return jsonify({"ok": True}), 200

    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 404

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@product_bp.route("/<id_product>", methods=["GET"])
def get_product(id_product):

    try:
        id_product = int(id_product)
        if id_product <= 0:
            return jsonify({"ok": False, "error": "El id ingresado debe ser positivo"}), 400

        product = ProductService.get_product_by_id(id_product)

        return jsonify({"ok": True, "product": product.to_dict()}), 200

    except ValueError as e:
        return jsonify({"ok": False, "error": "El id ingresado no existe"}), 404
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@product_bp.route("/<id_product>", methods=["PATCH"])
def update_product(id_product):
    try:
        id_product = int(id_product)

        if id_product <= 0:
            return jsonify({"ok": False, "error": "El id ingresado debe ser positivo"}), 400
        
        product = ProductService.update_product_by_id(id_product, request.json)
       
        return jsonify({"ok": True, "product": product.to_dict()}), 200
    
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

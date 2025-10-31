from flask import Blueprint, jsonify, request
from ...services.product.product_service import ProductService
from ...services.log.log_service import LogService
from utils.decorators import jwt_required_custom, role_required

product_bp = Blueprint("product", __name__, url_prefix="/products")


@product_bp.route("/", methods=["GET"])
@jwt_required_custom
def get_products():
    try:
        products = ProductService.get_all_products()
        return jsonify({"ok": True, "products": products}), 200

    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{get_products.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"ok": False, "error": str(e)}), 500


@product_bp.route("/", methods=["POST"])
@role_required([1])
def create_product():
    try:
        product = request.json
        new_product = ProductService.create_product_service(product)
        return jsonify({"ok": True, "product": new_product.to_dict()}), 201
    except (ValueError, TypeError) as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{create_product.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"ok": False, "error": str(e)}), 500


@product_bp.route("/<id_product>", methods=["DELETE"])
@role_required([1])
def delete_product(id_product):

    try:
        id_product = int(id_product)
        if id_product <= 0:
            return (
                jsonify({"ok": False, "error": "El id ingresado debe ser positivo"}),
                400,
            )

        ProductService.delete_product_by_id(id_product)

        return jsonify({"ok": True}), 200

    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 404

    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{delete_product.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"ok": False, "error": str(e)}), 500


@product_bp.route("/<id_product>", methods=["GET"])
@jwt_required_custom
def get_product(id_product):

    try:
        id_product = int(id_product)
        if id_product <= 0:
            return (
                jsonify({"ok": False, "error": "El id ingresado debe ser positivo"}),
                400,
            )

        product = ProductService.get_product_by_id(id_product)

        return jsonify({"ok": True, "product": product.to_dict()}), 200

    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 404

    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{get_product.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"ok": False, "error": str(e)}), 500


@product_bp.route("/<id_product>", methods=["PATCH"])
@role_required([1])
def update_product(id_product):
    try:
        id_product = int(id_product)

        if id_product <= 0:
            return (
                jsonify({"ok": False, "error": "El id ingresado debe ser positivo"}),
                400,
            )

        product = ProductService.update_product_by_id(id_product, request.json)

        return jsonify({"ok": True, "product": product.to_dict()}), 200

    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400

    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{update_product.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"ok": False, "error": str(e)}), 500

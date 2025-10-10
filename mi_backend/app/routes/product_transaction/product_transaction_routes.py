from flask import Blueprint, jsonify, request
from ...services.log.log_service import LogService
from ...services.product_transaction.product_transaction_service import (
    ProductTransactionService,
)

product_transaction_bp = Blueprint(
    "product_transaction", __name__, url_prefix="/product-transaction"
)


@product_transaction_bp.route("/", methods=["GET"])
def get_product_trasanctions():

    try:
        product_transactions = ProductTransactionService.get_all_products_transactions()

        return jsonify({"ok": True, "product_transactions": product_transactions}), 200

    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{get_product_trasanctions.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"ok": False, "error": str(e)}), 500


@product_transaction_bp.route("/<id_product_transaction>", methods=["GET"])
def get_product_transaction(id_product_transaction):

    try:
        product_transaction = ProductTransactionService.get_product_transaction_by_id(
            id_product_transaction
        )

        return jsonify({"ok": True, "product_transaction": product_transaction}), 200
    
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400

    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{get_product_transaction.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"ok": False, "error": str(e)}), 500


@product_transaction_bp.route("/", methods=["POST"])
def create_product_transaction():

    try:
        product_transaction = request.json

        new_product_transaction = (
            ProductTransactionService.create_product_transaction_service(
                product_transaction
            )
        )
        
        return jsonify({"ok": True, "product_transaction": new_product_transaction.to_dict()}), 201
    
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    
    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{create_product_transaction.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"ok": False, "error": str(e)}), 500
    

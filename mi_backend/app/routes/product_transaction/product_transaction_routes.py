from flask import Blueprint, jsonify, request, send_file
from ...services.log.log_service import LogService
from ...services.product_transaction.product_transaction_service import (
    ProductTransactionService,
)
from utils.decorators import jwt_required_custom, role_required

product_transaction_bp = Blueprint(
    "product_transaction", __name__, url_prefix="/product-transactions"
)


@product_transaction_bp.route("/", methods=["GET"])
@role_required([1])
def get_product_trasanctions():
    try:
        product_transactions = ProductTransactionService.get_all_products_transactions()

        return jsonify({"ok": True, "product_transactions": product_transactions}), 200

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)} ), 500


@product_transaction_bp.route("/<id_product_transaction>", methods=["GET"])
@role_required([1])
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
@jwt_required_custom
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


@product_transaction_bp.route("/report/excel", methods=["GET"])
@role_required([1])
def download_excel_report():
    """
    Endpoint para descargar el reporte de todas las transacciones en formato Excel
    """
    try:
        excel_file = ProductTransactionService.generate_excel_report()

        return send_file(
            excel_file,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='reporte_transacciones_productos.xlsx'
        )

    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{download_excel_report.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"ok": False, "error": str(e)}), 500

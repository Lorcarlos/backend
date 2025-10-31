from flask import Blueprint, jsonify
from ...services.log.log_service import LogService
from ...services.transaction_type.transaction_type_service import (
    TransactionTypeService,
)
from utils.decorators import jwt_required_custom

transaction_type_bp = Blueprint(
    "transaction_type", __name__, url_prefix="/transaction_types"
)


@transaction_type_bp.route("/", methods=["GET"])
@jwt_required_custom
def get_transaction_types():
    try:
        transaction_types = TransactionTypeService.get_all_transaction_types()
        return jsonify({"ok": True, "transaction_types": transaction_types}), 200
    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{get_transaction_types.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"ok": False, "error": str(e)}), 500


@transaction_type_bp.route("/<id_transaction_type>", methods=["GET"])
@jwt_required_custom
def get_transaction_type(id_transaction_type):

    try:
        id_transaction_type = int(id_transaction_type)
        if id_transaction_type <= 0:
            return (
                jsonify({"ok": False, "error": "El id ingresado debe ser positivo"}),
                400,
            )

        transaction_type = TransactionTypeService.get_transaction_type_by_id(
            id_transaction_type
        )

        return jsonify({"ok": True, "transaction_type": transaction_type}), 200

    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 404

    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{get_transaction_type.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"ok": False, "error": str(e)}), 500

from flask import Blueprint, jsonify, request
from ...database import db
from ...services.transaction_type.transaction_type_service import (
    Transaction_type_service,
)

transaction_type_bp = Blueprint(
    "transaction_type", __name__, url_prefix="/transaction_types"
)


@transaction_type_bp.route("/", methods=["GET"])
def get_transaction_types():
    try:
        transaction_types = Transaction_type_service.get_all_transaction_types()
        return jsonify({"ok": True, "transaction_types": transaction_types}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@transaction_type_bp.route("/<id_transaction_type>", methods=["GET"])
def get_transaction_type(id_transaction_type):

    try:
        id_transaction_type = int(id_transaction_type)
        if id_transaction_type <= 0:
            return (
                jsonify({"ok": False, "error": "El id ingresado debe ser positivo"}),
                400,
            )

        transaction_type = Transaction_type_service.get_transaction_type_by_id(
            id_transaction_type
        )

        return jsonify({"ok": True, "transaction_type": transaction_type}), 200

    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 404

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

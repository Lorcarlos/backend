from flask import Blueprint, jsonify, request
from ...services.supplier.supplier_service import SupplierService
from ...services.log.log_service import LogService
from flask_cors import CORS
from utils.decorators import jwt_required_custom, role_required

supplier_bp = Blueprint("supplier", __name__, url_prefix="/suppliers")

CORS(supplier_bp)


@supplier_bp.route("/", methods=["GET"])
@jwt_required_custom
def get_suppliers():

    try:
        suppliers = SupplierService.get_all_suppliers()
        return jsonify({"ok": True, "suppliers": suppliers}), 200

    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{get_suppliers.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"ok": False, "error": str(e)}), 500


@supplier_bp.route("/<id_supplier>", methods=["GET"])
@jwt_required_custom
def get_supplier(id_supplier):

    try:
        id_supplier = int(id_supplier)
        if id_supplier <= 0:
            return (
                jsonify({"ok": False, "error": "El id ingresado debe ser positivo"}),
                400,
            )

        supplier = SupplierService.get_supplier_by_id(id_supplier)

        return jsonify({"ok": True, "supplier": supplier.to_dict()}), 200

    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 404

    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{get_supplier.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"ok": False, "error": str(e)}), 500


@supplier_bp.route("/", methods=["POST"])
@role_required([1])
def create_supplier():

    try:
        supplier = request.json
        new_supplier = SupplierService.create_supplier(supplier)
        return jsonify({"ok": True, "supplier": new_supplier.to_dict()}), 201

    except (ValueError, TypeError) as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{create_supplier.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"ok": False, "error": str(e)}), 500


@supplier_bp.route("/<id_supplier>", methods=["PATCH"])
@role_required([1])
def update_supplier(id_supplier):

    try:
        id_supplier = int(id_supplier)

        if id_supplier <= 0:
            return (
                jsonify({"ok": False, "error": "El id ingresado debe ser positivo"}),
                400,
            )

        supplier = SupplierService.update_supplier_by_id(id_supplier, request.json)

        return jsonify({"ok": True, "supplier": supplier.to_dict()}), 200

    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400

    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{update_supplier.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"ok": False, "error": str(e)}), 500


@supplier_bp.route("/<id_supplier>", methods=["DELETE"])
@role_required([1])
def delete_supplier(id_supplier):

    try:
        id_supplier = int(id_supplier)

        if id_supplier <= 0:
            return (
                jsonify({"ok": False, "error": "El id ingresado debe ser positivo"}),
                400,
            )

        SupplierService.deleted_supplier_by_id(id_supplier)

        return jsonify({"ok": True}), 200

    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 404

    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{delete_supplier.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"ok": False, "error": str(e)}), 500

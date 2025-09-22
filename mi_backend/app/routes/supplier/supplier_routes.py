from flask import Blueprint, jsonify, request
from ...services.supplier.supplier_service import SupplierService

supplier_bp = Blueprint("supplier", __name__, url_prefix="/suppliers")


@supplier_bp.route("/", methods=["GET"])
def get_suppliers():

    try:
        suppliers = SupplierService.get_all_suppliers()
        return jsonify({"ok": True, "suppliers": suppliers}), 200

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@supplier_bp.route("/<id_supplier>", methods=["GET"])
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
        return jsonify({"ok": False, "error": str(e)}), 500


@supplier_bp.route("/", methods=["POST"])
def create_supplier():

    try:
        supplier = request.json
        new_supplier = SupplierService.create_supplier(supplier)
        return jsonify({"ok": True, "supplier": new_supplier.to_dict()}), 201

    except (ValueError, TypeError) as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@supplier_bp.route("/<id_supplier>", methods=["PATCH"])
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
        return jsonify({"ok": False, "error": str(e)}), 500


@supplier_bp.route("/<id_supplier>", methods=["DELETE"])
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
        return jsonify({"ok": False, "error": str(e)}), 500

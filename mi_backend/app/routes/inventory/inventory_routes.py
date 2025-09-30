from flask import Blueprint, jsonify, request
from ...services.inventory.inventory_service import InventoryService

inventory_bp = Blueprint("inventory", __name__, url_prefix="/inventories")


@inventory_bp.route("/", methods=["GET"])
def get_inventories():
    try:
        branch_id = request.args.get("branch_id", type=int)
        product_id = request.args.get("product_id", type=int)

        inventories = InventoryService.get_all_inventories(
            branch_id=branch_id, product_id=product_id
        )

        return jsonify({"ok": True, "inventories": inventories}), 200

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@inventory_bp.route("/<id_inventory>", methods=["GET"])
def get_inventory_by_id(id_inventory):
    try:
        id_inventory = int(id_inventory)

        if id_inventory <= 0:
            return (
                jsonify({"ok": False, "error": "El id ingresado debe ser positivo"}),
                400,
            )

        inventory = InventoryService.get_inventory_by_id(id_inventory)

        return jsonify({"ok": True, "inventory": inventory}), 200

    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 404

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


from flask import Blueprint, jsonify
from ...routes.rol.permissions import get_permissions

product_bp = Blueprint("product", __name__)

@product_bp.route("/permissions", methods=["GET"])
def get_permissions():

    data, status_code = get_permissions()

    if status_code == 200:
        return jsonify(data), status_code
    else:
        return jsonify(data), status_code
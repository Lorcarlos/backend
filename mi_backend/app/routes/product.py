from flask import Blueprint, jsonify
from ..database import db
from ..models import Product

product_bp = Blueprint("product", __name__)

@product_bp.route("/", methods=["GET"])
def test_db():
    try:
        products = Product.query.filter(
            Product.deleted_at.is_(None)
        ).all()
        products_list = [p.to_dict() for p in products]
        return jsonify({"ok":True, "products": products_list})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})
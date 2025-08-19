from flask import Blueprint, jsonify
from ..database import db
from ..models import Product

product_bp = Blueprint("product", __name__)

@product_bp.route("/test", methods=["GET"])
def test_db():
    try:
        products = Product.query.all()
        return jsonify({"ok":True, "count": len(products)})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})
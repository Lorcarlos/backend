from flask import Flask
from .database import init_db, db
from .routes.product.product_routes import product_bp
from .routes.transaction_type.transaction_type_routes import transaction_type_bp
from .routes.supplier.supplier_routes import supplier_bp
from .routes.company.company_routes import company_bp
from .routes.branch.branch_routes import branch_bp
from .routes.inventory.inventory_routes import inventory_bp

def create_app():
    app = Flask(__name__)
    init_db(app)

    # Registrar rutas
    app.register_blueprint(product_bp)
    app.register_blueprint(transaction_type_bp)
    app.register_blueprint(supplier_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(branch_bp)
    app.register_blueprint(inventory_bp)

    with app.app_context():
        db.create_all()

    return app

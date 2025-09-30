from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .database import init_db, db

# Importar los Blueprints
from .routes.product.product_routes import product_bp
from .routes.transaction_type.transaction_type_routes import transaction_type_bp
from .routes.supplier.supplier_routes import supplier_bp
from .routes.company.company_routes import company_bp
from .routes.branch.branch_routes import branch_bp
from .routes.inventory.inventory_routes import inventory_bp
from .routes.staff.staff_routes import personal_bp
from .routes.login.login_routes import auth_bp


def create_app():
    app = Flask(__name__)

    # 🔑 Configuración JWT
    app.config["JWT_SECRET_KEY"] = "super-secret-key"

    # Inicializar extensiones
    init_db(app)
    JWTManager(app)

    # ✅ CORS habilitado solo para tu frontend
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

    # Registrar Blueprints
    app.register_blueprint(product_bp)
    app.register_blueprint(transaction_type_bp)
    app.register_blueprint(supplier_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(branch_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(personal_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    return app

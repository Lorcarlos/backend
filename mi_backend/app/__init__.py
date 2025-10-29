from flask import Flask, request
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .database import init_db, db
from .smtp_config import init_smtp
import os
from datetime import timedelta

# Importar todos los modelos para que SQLAlchemy los reconozca
from .models import *

# Importar los Blueprints
from .routes.product.product_routes import product_bp
from .routes.transaction_type.transaction_type_routes import transaction_type_bp
from .routes.supplier.supplier_routes import supplier_bp
from .routes.company.company_routes import company_bp
from .routes.branch.branch_routes import branch_bp
from .routes.inventory.inventory_routes import inventory_bp
from .routes.staff.staff_routes import personal_bp
from .routes.login.login_routes import auth_bp
from .routes.log.log_routes import log_bp
from .routes.login_logs.user_logins_routes import user_logins_bp
from .routes.product_transaction.product_transaction_routes import (
    product_transaction_bp,
)


def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-key")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

    init_db(app)
    JWTManager(app)
    init_smtp(app)

    CORS(
        app,
        resources={
            r"/*": {
                "origins": [
                    "http://localhost:5173",
                    "https://*.trycloudflare.com"
                ],         
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True
            }
        }
    )

    @app.before_request
    def handle_options():
        if request.method == "OPTIONS":
            response = app.make_response('')
            response.status_code = 200
            return response

    # Registrar blueprints
    app.register_blueprint(product_bp)
    app.register_blueprint(transaction_type_bp)
    app.register_blueprint(supplier_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(branch_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(personal_bp)
    app.register_blueprint(product_transaction_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(log_bp)
    app.register_blueprint(user_logins_bp)

    with app.app_context():
        db.create_all()

    return app

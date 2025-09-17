from flask import Flask
from .database import init_db, db
from .routes.product.product_routes import product_bp

def create_app():
    app = Flask(__name__)
    init_db(app)

    # Importar modelos
    from . import services

    # Registrar rutas
    app.register_blueprint(product_bp, url_prefix="/products")

    with app.app_context():
        db.create_all()

    return app

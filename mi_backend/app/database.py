import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

db = SQLAlchemy()


def init_db(app):
    load_dotenv()

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Evita usar conexiones muertas
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,  # chequea que la conexión siga viva antes de usarla
        "pool_recycle": 280,  # recicla conexiones cada 5 min (antes del timeout del servidor)
        "pool_timeout": 30,  # espera máx. 30 seg al obtener conexión del pool
        "pool_size": 5,
        "max_overflow": 10,
    }

    db.init_app(app)

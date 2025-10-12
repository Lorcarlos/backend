import os
from flask_mail import Mail
from dotenv import load_dotenv

load_dotenv()

mail = Mail()

def init_smtp(app):
    
    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
    app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL", "False").lower() == "true"
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    
    # Configurar el remitente por defecto
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_USERNAME")
    
    # Configuraciones adicionales para evitar problemas SSL
    app.config["MAIL_DEBUG"] = False
    app.config["MAIL_SUPPRESS_SEND"] = False

    mail.init_app(app)
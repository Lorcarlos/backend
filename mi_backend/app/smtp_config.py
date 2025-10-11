import os
from flask_mail import Mail
from dotenv import load_dotenv

load_dotenv()

mail = Mail()

def init_smtp(app):
    
    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_PORT"] = os.getenv("MAIL_PORT")
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS")
    app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL")
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

    mail.init_app(app)
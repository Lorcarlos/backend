from flask_mail import Message
from flask import current_app
from ..smtp_config import mail
import logging


def send_otp_mail(subject, recipient, body):
    try:
        if isinstance(recipient, str):
            recipient = [recipient]  # Flask-Mail espera una lista

        msg = Message(
            subject=subject,
            recipients=recipient,
            body=body,
            sender=current_app.config.get('MAIL_DEFAULT_SENDER')
        )    
        
        mail.send(msg)
        
        return 'Correo enviado con éxito'
    
    except Exception as e:
        logging.error(f"Error enviando correo: {str(e)}")
        raise Exception(f"Error al enviar correo: {str(e)}")


from flask_mail import Message
from ..smtp_config import mail


def send_otp_mail(subject, recipient, body):
    
    if isinstance(recipient, str):
        recipient = [recipient]  # Flask-Mail espera una lista

    msg = Message(
        subject= subject,
        recipients=recipient,
        body= body
    )    
    
    mail.send(msg)
    
    return 'Correo enviado con éxito'


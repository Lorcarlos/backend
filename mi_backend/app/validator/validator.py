import re
from ..models.staff.staff_peticion import AppUser
from werkzeug.security import generate_password_hash
# Expresiones regulares generales
regex_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
regex_nit = r"^\d{9}$"
regex_phone_number = r"^\+?\d{7,15}$"


def validate_data(data, required_fields):

    for field in required_fields:
        if field not in data or data.get(field) is None or data.get(field) == "":
            raise ValueError(
                f"El campo '{field}' es obligatorio y no puede estar vacío."
            )

    for field, expected_type in required_fields.items():
        if not isinstance(data.get(field), expected_type):
            raise TypeError(
                f"El campo '{field}' debe ser de tipo '{expected_type.__name__}'."
            )

    return True


def validate_supplier_data(supplier):
    """
    Validaciones específicas para proveedores.
    """
    for key, value in supplier.items():

        if key in ("name", "contact_name"):
            if len(value) < 3:
                raise ValueError(
                    f"El {key} del proveedor no puede ser menor a 3 caracteres."
                )

        if key in ("address", "description"):
            if len(value) < 5:
                raise ValueError(
                    f"La {key} del proveedor no puede ser menor a 5 caracteres."
                )

        if key == "nit":
            if not re.match(regex_nit, value):
                raise ValueError(f"El {key} del proveedor no es válido.")

        if key == "phone_number":
            if not re.match(regex_phone_number, value):
                raise ValueError(f"El {key} del proveedor no es válido.")

        if key == "email":
            if not re.match(regex_email, value):
                raise ValueError(f"El {key} del proveedor no es válido.")


def validate_phone_number(phone_number: int):
    phone_str = str(phone_number)

    if not phone_str.isdigit():
        raise ValueError("El número de teléfono debe contener solo dígitos.")

    if len(phone_str) != 10:
        raise ValueError("El número de teléfono debe tener exactamente 10 dígitos.")

    if not phone_str.startswith("3"):
        raise ValueError("El número de teléfono debe empezar con '3'.")

    return True


def validate_document_id(document_id: int):
    doc_str = str(document_id)

    if not doc_str.isdigit():
        raise ValueError("El document_id debe contener solo números.")

    if not (8 <= len(doc_str) <= 12):
        raise ValueError("El document_id debe tener entre 8 y 12 dígitos.")

    return True


def validate_unique_email(email: str):
    existing = AppUser.query.filter_by(email=email).first()
    if existing:
        raise ValueError(f"El email '{email}' ya está registrado.")
    return True


def validate_unique_document_id(document_id: int):
    existing = AppUser.query.filter_by(document_id=document_id).first()
    if existing:
        raise ValueError(f"El documento '{document_id}' ya está registrado.")
    return True



def hash_password(password_plain):
    if not password_plain:
        return None
    return generate_password_hash(password_plain)
import re
from ..models.staff.staff_peticion import AppUser
from werkzeug.security import generate_password_hash


# Expresiones regulares generales
regex_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
regex_nit = r"^\d{9}$"
regex_phone_number = r"^3\d{9}$"
regex_document_id = r"^\d{6,10}$"


def validate_data(data, required_fields):

    for field in required_fields:
        if field not in data or data.get(field) is None or data.get(field) == "":
            raise ValueError(
                f"El campo '{field}' es obligatorio y no puede estar vacío."
            )

    for field, expected_type in required_fields.items():
        value = data.get(field)

        # Caso especial para IDs: debe ser convertible a int
        if field.endswith("_id") and isinstance(value, str):
            try:
                int(value)
            except (ValueError, TypeError):
                raise ValueError(f"El campo '{field}' debe ser un número válido")

        if not isinstance(value, expected_type):
            # Manejar tuplas de tipos
            if isinstance(expected_type, tuple):
                type_names = [t.__name__ for t in expected_type]
                raise TypeError(
                    f"El campo '{field}' debe ser de tipo '{' o '.join(type_names)}'."
                )
            else:
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

    if not re.match(regex_phone_number, phone_str):
        raise ValueError(f"El número de teléfono no es válido.")

    return True


def validate_document_id(document_id: int):
    doc_str = str(document_id)

    if not re.match(regex_document_id, doc_str):
        raise ValueError("El document_id no es válido.")

    return True


def hash_password(password_plain):
    if not password_plain:
        return None
    return generate_password_hash(password_plain)

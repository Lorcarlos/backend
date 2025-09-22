import re

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

    for key, value in supplier.items():

        if key == "name" or key == "contact_name":
            if len(value) < 3:
                raise ValueError(
                    f"El {key} del proveedor no puede ser menor a 3 caracteres"
                )

        if key == "address" or key == "description":
            if len(value) < 5:
                raise ValueError(
                    f"La {key} del proveedor no puede ser menor a 5 caracteres"
                )

        if key == "nit":
            if not re.match(regex_nit, value):
                raise ValueError(f"El {key} del proveedor no es válido")

        if key == "phone_number":
            if not re.match(regex_phone_number, value):
                raise ValueError(f"El {key} del proveedor no es válido")

        if key == "email":
            if not re.match(regex_email, value):
                raise ValueError(f"El {key} del proveedor no es válido")

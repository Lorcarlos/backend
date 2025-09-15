
def validate_data(data, required_fields):

    for field in required_fields:
        if field not in data or data.get(field) is None or data.get(field) == '':
            raise ValueError(f"El campo '{field}' es obligatorio y no puede estar vacío.")

    for field, expected_type in required_fields.items():
        if not isinstance(data.get(field), expected_type):
            raise TypeError(f"El campo '{field}' debe ser de tipo '{expected_type.__name__}'.")

    return True
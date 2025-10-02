from datetime import datetime

def parse_transaction_date(date_input):
    """
    Convierte una fecha de string a datetime object.
    Solo acepta formatos estándar: YYYY-MM-DD, DD/MM/YYYY, DD-MM-YYYY
    """
    if isinstance(date_input, datetime):
        return date_input

    if isinstance(date_input, str):
        # Formatos soportados
        date_formats = [
            "%Y-%m-%d",  # 2025-08-15
            "%d/%m/%Y",  # 15/08/2025
            "%d-%m-%Y",  # 15-08-2025
            "%Y/%m/%d",  # 2025/08/15
        ]

        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(date_input, fmt)
                return parsed_date
            except ValueError:
                continue

        # Si no coincide con ningún formato, lanzar error
        raise ValueError(
            f"Formato de fecha inválido: '{date_input}'. Use formatos: YYYY-MM-DD, DD/MM/YYYY, DD-MM-YYYY, o YYYY/MM/DD"
            )

    # Si no es string ni datetime, lanzar error
    raise ValueError("La fecha debe ser un string en formato válido")

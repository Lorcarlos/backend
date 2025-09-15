import database

roles = """SELECT * FROM role"""

# Consultas para el CRUD de personal
PERSONAS_QUERY = "SELECT id, name, phone, email, address FROM persons WHERE deleted_at IS NULL"
PERSONA_POR_ID_QUERY = "SELECT id, name, phone, email, address FROM persons WHERE id = %s AND deleted_at IS NULL"
CREAR_PERSONA_QUERY = "INSERT INTO persons (name, phone, email, address) VALUES (%s, %s, %s, %s)"
ACTUALIZAR_PERSONA_QUERY = "UPDATE persons SET name = %s, phone = %s, email = %s, address = %s WHERE id = %s"
ELIMINAR_PERSONA_QUERY = "UPDATE persons SET deleted_at = NOW() WHERE id = %s"

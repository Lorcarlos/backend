# app/models/personal/Personal.py

from database import get_connection
from const import const

def get_all_personal():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(const.PERSONAS_QUERY)
        personal_list = cursor.fetchall()
        cursor.close()
        conn.close()
        return personal_list
    except Exception as e:
        raise Exception(f"Error al obtener personal: {str(e)}")

def get_personal_by_id(person_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(const.PERSONA_POR_ID_QUERY, (person_id,))
        person = cursor.fetchone()
        cursor.close()
        conn.close()
        return person
    except Exception as e:
        raise Exception(f"Error al obtener personal por ID: {str(e)}")

def create_personal(data):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(const.CREAR_PERSONA_QUERY, )
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return last_id
    except Exception as e:
        if 'Duplicate entry' in str(e):
            raise Exception("El email ya existe")
        raise Exception(f"Error al crear personal: {str(e)}")

def update_personal(person_id, data):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        values = (data.get("name"), data.get("phone"), data.get("email"), data.get("address"), person_id)
        cursor.execute(const.ACTUALIZAR_PERSONA_QUERY, values)
        conn.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        conn.close()
        return rows_affected > 0
    except Exception as e:
        raise Exception(f"Error al actualizar personal: {str(e)}")

def delete_personal(person_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(const.ELIMINAR_PERSONA_QUERY, (person_id,))
        conn.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        conn.close()
        return rows_affected > 0
    except Exception as e:
        raise Exception(f"Error al eliminar personal: {str(e)}")
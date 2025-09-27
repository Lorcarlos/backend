from ...database import db
from datetime import datetime
from ...models.staff.staff_peticion import AppUser
from ...validator.validator import (
    validate_data,
    validate_phone_number,
    validate_document_id,
    validate_unique_email,
    validate_unique_document_id,
    hash_password
)

def create_new_user(data: dict) -> AppUser:
    required_fields = {
        "name": str,
        "email": str,
        "username": str,
        "hashed_password": str,
        "document_id": int,
        "phone_number": int,
        "role_id": int,
        "branch_id": int
    }

    # Validaciones
    validate_data(data, required_fields)
    validate_phone_number(data["phone_number"])
    validate_document_id(data["document_id"])
    validate_unique_email(data["email"])        
    validate_unique_document_id(data["document_id"]) 

    new_user = AppUser(
        name=data["name"],
        email=data["email"],
        username=data["username"],
        hashed_password=hash_password(data["hashed_password"]),
        document_id=data["document_id"],
        phone_number=data["phone_number"],
        role_id=data["role_id"],
        branch_id=data["branch_id"]
    )

    db.session.add(new_user)
    db.session.commit()

    return new_user


def soft_delete_user_if_requested(document_id):
    user = AppUser.query.filter_by(document_id=document_id).first()
    if not user:
        return False

    user.deleted_at = datetime.utcnow()
    db.session.commit()
    return True


def update_user_service(document_id, data):
    if not data:
        return {"ok": False, "error": "No se proporcionaron datos", "status": 400}

    allowed_fields = {
        "name": str,
        "email": str,
        "username": str,         
        "hashed_password": str,
        "phone_number": int,
        "role_id": int,
        "branch_id": int
    }

    update_data = {}
    for field, field_type in allowed_fields.items():
        if field in data:
            try:
                update_data[field] = field_type(data[field])
            except (ValueError, TypeError):
                return {"ok": False, "error": f"Tipo inválido para {field}", "status": 400}

    if not update_data:
        return {"ok": False, "error": "No se proporcionaron campos válidos para actualizar", "status": 400}

    user = AppUser.query.filter_by(document_id=document_id, deleted_at=None).first()
    if not user:
        return {"ok": False, "error": "Usuario no encontrado", "status": 404}


    if "email" in update_data:
        existing_email_user = AppUser.query.filter_by(email=update_data["email"]).first()
        if existing_email_user and existing_email_user.document_id != document_id:
            return {"ok": False, "error": "El email ya está en uso por otro usuario", "status": 400}

    if "username" in update_data:
        existing_username_user = AppUser.query.filter_by(username=update_data["username"]).first()
        if existing_username_user and existing_username_user.document_id != document_id:
            return {"ok": False, "error": "El username ya está en uso por otro usuario", "status": 400}

    # Si hay contraseña, aplicamos hash
    if "hashed_password" in update_data:
        update_data["hashed_password"] = hash_password(update_data["hashed_password"])

    # Actualizamos campos
    for field, value in update_data.items():
        setattr(user, field, value)

    user.updated_at = datetime.utcnow()
    db.session.commit()

    return {"ok": True, "message": "Usuario actualizado correctamente", "document_id": document_id, "status": 200}

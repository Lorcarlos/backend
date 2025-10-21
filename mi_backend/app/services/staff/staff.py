from ...database import db
from datetime import datetime, timezone
from ...models.staff.staff_peticion import AppUser
from ...services.log.log_service import LogService
from ...utils.validator import (
    validate_data,
    validate_phone_number,
    validate_document_id,
    hash_password,
)
from ...utils.soft_delete_handler import SoftDeleteHandler
from sqlalchemy import or_


@staticmethod
def create_new_user(data: dict) -> AppUser:
    required_fields = {
        "name": str,
        "email": str,
        "username": str,
        "hashed_password": str,
        "document_id": int,
        "phone_number": int,
        "role_id": int,
        "branch_id": int,
    }

    # Establecer is_active por defecto si no se envía
    if "is_active" not in data:
        data["is_active"] = True

    # Validaciones básicas
    validate_data(data, required_fields)
    validate_phone_number(data["phone_number"])
    validate_document_id(data["document_id"])

    # Llama al handler que verifica si el elemento existe y está activo o si existe y está soft_deleted
    return SoftDeleteHandler.create_or_restore(
        model=AppUser,
        unique_filters=or_(
            AppUser.email == data["email"],
            AppUser.document_id == data["document_id"],
            AppUser.username == data["username"],
        ),
        data=data,
        restore_fn=restore_deleted_user,
        create_fn=create_fresh_user,
    )


@staticmethod
def get_user_by_id(user_id):

    user = AppUser.query.filter(
        AppUser.deleted_at.is_(None), AppUser.id == user_id
    ).first()

    if user is None:
        LogService.create_log(
            {
                "module": f"{get_user_by_id.__name__}",
                "message": "No se encontró el usuario buscado por id",
            }
        )
        raise ValueError("Usuario no encontrado")

    return user


@staticmethod
def serialize_user(user: AppUser) -> dict:
    """Serializa un objeto AppUser a un diccionario con el formato esperado por el frontend"""
    # Mapeo de role_id a nombre de rol
    role_map = {
        1: "Administrador",
        2: "Usuario",
        3: "Gerente",
    }

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "username": user.username,
        "document_id": str(user.document_id),
        "phone_number": str(user.phone_number),
        "role": role_map.get(user.role_id, "Usuario"),
        "cargo": role_map.get(user.role_id, "Usuario"),  # cargo es lo mismo que role
        "branch_id": user.branch_id,
        "deleted_at": user.deleted_at.isoformat() if user.deleted_at else None,
    }


@staticmethod
def get_user_by_email(email):

    user = AppUser.query.filter(AppUser.email == email, AppUser.deleted_at.is_(None)).first()

    if user is None:
        LogService.create_log(
            {
                "module": f"{get_user_by_email.__name__}",
                "message": "No se encontró el usuario buscado por email",
            }
        )
        raise ValueError("Usuario no encontrado")

    return user


@staticmethod
def soft_delete_user_if_requested(document_id):
    user = AppUser.query.filter_by(document_id=document_id).first()
    if not user:
        return False

    user.deleted_at = datetime.utcnow()
    db.session.commit()
    return True


@staticmethod
def update_user_service(document_id, data):
    if not data:
        return {"ok": False, "error": "No se proporcionaron datos", "status": 400}

    # Manejar new_password si viene del frontend
    if "new_password" in data:
        data["hashed_password"] = data.pop("new_password")

    allowed_fields = {
        "name": str,
        "email": str,
        "username": str,
        "hashed_password": str,
        "document_id": str,
        "phone_number": int,
        "role_id": int,
        "branch_id": int,
    }

    update_data = {}
    for field, field_type in allowed_fields.items():
        if field in data:
            try:
                update_data[field] = field_type(data[field])
            except (ValueError, TypeError):
                return {
                    "ok": False,
                    "error": f"Tipo inválido para {field}",
                    "status": 400,
                }

    if not update_data:
        return {
            "ok": False,
            "error": "No se proporcionaron campos válidos para actualizar",
            "status": 400,
        }

    user = AppUser.query.filter_by(document_id=document_id, deleted_at=None).first()
    if not user:
        return {"ok": False, "error": "Usuario no encontrado", "status": 404}

    if "email" in update_data:
        existing_email_user = AppUser.query.filter_by(
            email=update_data["email"]
        ).first()
        if existing_email_user and existing_email_user.document_id != document_id:
            return {
                "ok": False,
                "error": "El email ya está en uso por otro usuario",
                "status": 400,
            }

    if "username" in update_data:
        existing_username_user = AppUser.query.filter_by(
            username=update_data["username"]
        ).first()
        if existing_username_user and existing_username_user.document_id != document_id:
            return {
                "ok": False,
                "error": "El username ya está en uso por otro usuario",
                "status": 400,
            }

    if "document_id" in update_data:
        existing_document_user = AppUser.query.filter_by(
            document_id=update_data["document_id"]
        ).first()
        if existing_document_user and existing_document_user.document_id != document_id:
            return {
                "ok": False,
                "error": "El document_id ya está en uso por otro usuario",
                "status": 400,
            }

    # Si hay contraseña, aplicamos hash
    if "hashed_password" in update_data:
        update_data["hashed_password"] = hash_password(update_data["hashed_password"])

    # Actualizamos campos
    for field, value in update_data.items():
        setattr(user, field, value)

    user.updated_at = datetime.utcnow()
    db.session.commit()

    # Serializar el usuario actualizado para devolverlo
    user_data = serialize_user(user)

    return {
        "ok": True,
        "message": "Usuario actualizado correctamente",
        "user": user_data,
        "status": 200,
    }


@staticmethod
def restore_deleted_user(existing_user: AppUser, new_data: dict) -> AppUser:
    """Restaura usuario eliminado actualizando todos los campos pero manteniendo created_at original"""
    # Actualizar todos los campos de datos
    existing_user.name = new_data["name"]
    existing_user.email = new_data["email"]
    existing_user.username = new_data["username"]
    existing_user.hashed_password = hash_password(new_data["hashed_password"])
    existing_user.document_id = new_data["document_id"]
    existing_user.phone_number = new_data["phone_number"]
    existing_user.role_id = new_data["role_id"]
    existing_user.branch_id = new_data["branch_id"]
    existing_user.is_active = new_data.get("is_active", True)

    # Solo actualizar updated_at y limpiar deleted_at
    existing_user.updated_at = datetime.now(timezone.utc)
    existing_user.deleted_at = None
    # created_at se mantiene igual (cuándo se creó originalmente)

    db.session.commit()
    return existing_user


@staticmethod
def create_fresh_user(data: dict) -> AppUser:
    """Crea un usuario completamente nuevo"""
    new_user = AppUser(
        name=data["name"],
        email=data["email"],
        username=data["username"],
        hashed_password=hash_password(data["hashed_password"]),
        document_id=data["document_id"],
        phone_number=data["phone_number"],
        role_id=data["role_id"],
        branch_id=data["branch_id"],
        is_active=data.get("is_active", True),
    )

    db.session.add(new_user)
    db.session.commit()

    return new_user

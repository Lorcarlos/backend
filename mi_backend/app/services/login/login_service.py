from ...models.staff.staff_peticion import AppUser
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from flask import jsonify  

from sqlalchemy import or_

def login(username, password):
   
    user = AppUser.query.filter_by(username=username).filter(AppUser.deleted_at.is_(None)).first()

    if not user:
        return jsonify({"error": "Usuario no encontrado "}), 404

    if not check_password_hash(user.hashed_password, password):
        return jsonify({"error": "Contraseña incorrecta"}), 401

    access_token = create_access_token(identity={
        "username": user.username,
        "role": user.role_id
    })

    return jsonify({
        "message": "Login exitoso",
        "access_token": access_token,
        "username": user.username,
        "role": user.role_id,
        "branch_id": user.branch_id 
    }), 200

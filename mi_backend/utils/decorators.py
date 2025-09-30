from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
from flask import jsonify

def role_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            user_role = claims.get("role")
            is_active = claims.get("is_active", True)

            # Validar si el usuario está activo
            if not is_active:
                return jsonify({"error": "Usuario inactivo"}), 403

            # Validar el rol
            if user_role not in roles:
                return jsonify({"error": "Acceso denegado"}), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper

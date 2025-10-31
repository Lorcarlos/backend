from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
from flask import jsonify

def jwt_required_custom(fn):
    """Decorador simple que solo requiere autenticacion JWT valida"""
    @wraps(fn)
    def decorator(*args, **kwargs):
        try:
            verify_jwt_in_request()
            claims = get_jwt()

            is_active = claims.get("is_active", True)

            if not is_active:
                return jsonify({"ok": False, "error": "Usuario inactivo"}), 403

            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({"ok": False, "error": "Token invalido o expirado"}), 401
    return decorator

def role_required(roles):
    """Decorador que requiere autenticacion JWT y valida roles especificos

    Args:
        roles: lista de role_ids permitidos (ej: [1] para solo admin, [1,2] para admin y empleado)
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
                claims = get_jwt()

                user_role = claims.get("role")
                is_active = claims.get("is_active", True)

                # Validar si el usuario está activo
                if not is_active:
                    return jsonify({"ok": False, "error": "Usuario inactivo"}), 403

                # Validar el rol
                if user_role not in roles:
                    return jsonify({"ok": False, "error": "Acceso denegado. Permisos insuficientes"}), 403

                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({"ok": False, "error": "Token invalido o expirado"}), 401
        return decorator
    return wrapper

# Documentación de Rate Limiting

## Resumen

Se ha implementado un sistema de rate limiting (limitación de intentos) para proteger los endpoints de autenticación contra ataques de fuerza bruta.

## Endpoints Protegidos

### 1. Login (POST /auth/login)
- **Límite**: 5 intentos fallidos
- **Bloqueo**: 30 minutos
- **Identificador**: username
- **Reset automático**: 15 minutos sin intentos

### 2. Verificación OTP de Login (POST /auth/verify-otp)
- **Límite**: 3 intentos fallidos
- **Bloqueo**: 15 minutos
- **Identificador**: username
- **Reset automático**: 15 minutos sin intentos

### 3. Verificación OTP de Reset Password (POST /auth/verify-otp-password)
- **Límite**: 3 intentos fallidos
- **Bloqueo**: 15 minutos
- **Identificador**: email
- **Reset automático**: 15 minutos sin intentos

## Funcionamiento

### Flujo Normal

1. **Intento Fallido**:
   - Se registra el intento en la tabla `rate_limit`
   - Se retorna un error con el mensaje: "Credenciales inválidas" o "El token ingresado no existe"
   - El contador de intentos aumenta

2. **Intento Exitoso**:
   - Se resetean todos los contadores para ese identificador/endpoint
   - El usuario puede autenticarse normalmente

3. **Bloqueo**:
   - Cuando se alcanza el límite máximo de intentos
   - Se establece un `blocked_until` timestamp
   - Mensaje de error: "Demasiados intentos fallidos. Cuenta bloqueada por X minutos"

4. **Durante el Bloqueo**:
   - Cualquier intento retorna inmediatamente
   - Mensaje: "Cuenta bloqueada temporalmente. Intenta nuevamente en X minutos"

5. **Desbloqueo Automático**:
   - Después de transcurrido el tiempo de bloqueo
   - O después de 15 minutos sin intentos (auto-reset)

## Mensajes de Error para el Frontend

Los mensajes de error que recibirá el frontend son:

### Login:
- Normal: `"Credenciales inválidas"`
- Bloqueado: `"Demasiados intentos fallidos. Cuenta bloqueada por 30 minutos"`
- Durante bloqueo: `"Cuenta bloqueada temporalmente. Intenta nuevamente en X minutos"`

### Verify OTP:
- Normal: `"El token ingresado no existe"` o `"El usuario ingresado no existe"`
- Bloqueado: `"Demasiados intentos fallidos. Cuenta bloqueada por 15 minutos"`
- Durante bloqueo: `"Cuenta bloqueada temporalmente. Intenta nuevamente en X minutos"`

### Verify OTP Password:
- Normal: `"El token ingresado no existe"` o `"El email ingresado no existe"`
- Bloqueado: `"Demasiados intentos fallidos. Cuenta bloqueada por 15 minutos"`
- Durante bloqueo: `"Cuenta bloqueada temporalmente. Intenta nuevamente en X minutos"`

## Logging

Todos los intentos (exitosos y fallidos) se registran en la tabla `log` con:
- Módulo que generó el evento
- Tipo de fallo (usuario no existe, token inválido, bloqueado, etc.)
- Identificador (username o email)
- Intentos restantes

## Seguridad Adicional

### Ventajas del Sistema:
1. **Protección contra fuerza bruta**: Limita intentos automáticos
2. **Protección contra enumeración de usuarios**: No se distingue entre "usuario no existe" y "contraseña incorrecta"
3. **Auto-recuperación**: Se desbloquea automáticamente sin intervención manual
4. **Trazabilidad**: Todos los intentos quedan registrados en logs
5. **Granular por endpoint**: Login y OTP tienen límites independientes

### Recomendaciones:
- Los mensajes genéricos previenen que atacantes sepan si un username/email existe
- Los tiempos de bloqueo son suficientemente largos para desincentivar ataques automatizados
- El reset automático después de 15 minutos sin actividad previene bloqueos permanentes por error

## Desbloqueo Manual (Si se necesita en el futuro)

Si necesitas desbloquear manualmente un usuario, ejecuta:

```sql
-- Desbloquear por username
DELETE FROM rate_limit WHERE identifier = 'username_aqui';

-- Desbloquear por email
DELETE FROM rate_limit WHERE identifier = 'email@example.com';

-- Ver intentos actuales
SELECT * FROM rate_limit WHERE identifier = 'username_aqui';
```

## Testing

Para probar el sistema:

1. **Test de Login**:
   - Intenta hacer login con contraseña incorrecta 5 veces
   - El 5to intento debe bloquear por 30 minutos
   - Intentos adicionales deben mostrar tiempo restante

2. **Test de OTP**:
   - Haz login correcto para recibir OTP
   - Ingresa código incorrecto 3 veces
   - El 3er intento debe bloquear por 15 minutos

3. **Test de Reset Password OTP**:
   - Solicita reset de contraseña
   - Ingresa código incorrecto 3 veces
   - El 3er intento debe bloquear por 15 minutos

4. **Test de Auto-reset**:
   - Haz 2 intentos fallidos
   - Espera 15 minutos sin intentos
   - El contador debe resetearse automáticamente

# ImproExpress - Sistema de Gestión de Inventario - Backend API

Sistema de gestión de inventario empresarial desarrollado con Flask, SQLAlchemy y MySQL. Proporciona una API REST completa para la administración de productos, inventarios, transacciones, personal y autenticación con OTP por correo electrónico.

## Características Principales

### Arquitectura del Backend
- **Patrón Arquitectónico**: Service Layer Architecture (Arquitectura en 3 capas)
  - **Routes (Controllers)**: Manejo de peticiones HTTP y respuestas
  - **Services**: Lógica de negocio, validaciones y procesamiento
  - **Models**: Modelos de datos con SQLAlchemy ORM
- **Tipo de API**: REST API (retorna JSON, no HTML)
- **Framework**: Flask 2.3.2
- **ORM**: SQLAlchemy 3.0.5
- **Base de Datos**: MySQL con PyMySQL
- **Autenticación**: JWT (JSON Web Tokens) con OTP por correo
- **Correo Electrónico**: Flask-Mail con SMTP de Gmail
- **Validación**: Regex y validaciones personalizadas en capa de servicios
- **CORS**: Configurado para integración con frontend React

### Modelos de Base de Datos
- **AppUser**: Gestión de usuarios del sistema con roles y sucursales
- **Company**: Gestión de empresas
- **Branch**: Sucursales de las empresas
- **Product**: Catálogo de productos con precios y descripciones
- **Supplier**: Proveedores con información de contacto
- **Inventory**: Control de inventario por sucursal y producto
- **TransactionType**: Tipos de transacciones (entrada/salida)
- **ProductTransaction**: Transacciones de productos con historial completo
- **Token**: Tokens OTP para autenticación de dos factores
- **UserLogins**: Registro de inicios de sesión
- **Log**: Sistema de logging para auditoría

### Funcionalidades Implementadas
- **Autenticación de Dos Factores**: Login con OTP enviado por correo
- **CRUD completo** para todas las entidades
- **Soft delete** implementado en todas las tablas
- **Validación robusta** de datos con expresiones regulares
- **Sistema de roles** y permisos
- **Envío de correos** SMTP con Flask-Mail
- **Sistema de logging** para auditoría
- **API REST** con respuestas JSON estandarizadas
- **Generación de reportes Excel** con openpyxl
- **Manejo de errores** consistente
- **CORS configurado** para integración con frontend
- **Gestión de inventario** con actualizaciones automáticas
- **JWT con expiración de 1 hora**

## Estructura del Proyecto

```
mi_backend/
├── app/
│   ├── models/              # Modelos de SQLAlchemy
│   │   ├── company/
│   │   ├── branch/
│   │   ├── product/
│   │   ├── supplier/
│   │   ├── inventory/
│   │   ├── transaction_type/
│   │   ├── product_transaction/
│   │   ├── staff/
│   │   ├── token/
│   │   ├── login_logs/
│   │   └── log/
│   ├── routes/              # Endpoints de la API
│   │   ├── company/
│   │   ├── branch/
│   │   ├── product/
│   │   ├── supplier/
│   │   ├── inventory/
│   │   ├── transaction_type/
│   │   ├── product_transaction/
│   │   ├── staff/
│   │   ├── login/
│   │   ├── login_logs/
│   │   └── log/
│   ├── services/            # Lógica de negocio
│   │   ├── company/
│   │   ├── branch/
│   │   ├── product/
│   │   ├── supplier/
│   │   ├── inventory/
│   │   ├── transaction_type/
│   │   ├── product_transaction/
│   │   ├── staff/
│   │   ├── login/
│   │   ├── token/
│   │   ├── login_logs/
│   │   └── log/
│   ├── utils/               # Utilidades y helpers
│   │   ├── mail_sender.py
│   │   ├── tokenGenerator.py
│   │   ├── tokenType.py
│   │   ├── validator.py
│   │   └── date_conversor.py
│   ├── smtp_config.py       # Configuración SMTP
│   ├── database.py          # Configuración de base de datos
│   └── __init__.py          # Inicialización de la aplicación
├── instance/                # Instancia de base de datos
├── tests/                   # Tests del proyecto
├── utils/                   # Utilidades adicionales
├── venv/                    # Entorno virtual
├── requirements.txt         # Dependencias del proyecto
├── run.py                   # Punto de entrada de la aplicación
├── .env                     # Variables de entorno
├── .gitignore              # Archivos ignorados por Git
└── README.md               # Documentación del proyecto
```

## Instalación y Configuración

### Prerrequisitos
- Python 3.11.9
- MySQL 5.7 o superior
- pip (gestor de paquetes de Python)
- Cuenta de Gmail con verificación en 2 pasos habilitada

### 1. Clonar el Repositorio
```bash
git clone <url-del-repositorio>
cd improexpress_app/backend/mi_backend
```

### 2. Crear Entorno Virtual
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
Crear archivo `.env` en la raíz del proyecto:
```env
FLASK_ENV=development
JWT_SECRET="jwt_super_secreto"
DATABASE_URI="mysql+pymysql://impro_user:Pa55w.rd@127.0.0.1/improexpress_database"

# CONFIGURACIÓN SMTP
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=contraseña_de_aplicación_de_16_caracteres
```

### 5. Configurar Gmail para SMTP
1. Habilitar **Verificación en 2 pasos** en tu cuenta de Google
2. Generar una **Contraseña de aplicación** específica para esta aplicación
3. Usar esa contraseña en `MAIL_PASSWORD` (no tu contraseña normal)

### 6. Configurar Base de Datos
1. Crear la base de datos en MySQL:
```sql
CREATE DATABASE improexpress_database;
CREATE USER 'impro_user'@'localhost' IDENTIFIED BY 'Pa55w.rd';
GRANT ALL PRIVILEGES ON improexpress_database.* TO 'impro_user'@'localhost';
FLUSH PRIVILEGES;
```

2. Ejecutar la aplicación para crear las tablas automáticamente:
```bash
python run.py
```

### 7. Ejecutar la Aplicación
```bash
python run.py
```

La aplicación estará disponible en `http://localhost:5000`

## API Endpoints

### Autenticación
- `POST /auth/login` - Iniciar sesión (envía OTP por correo)
- `POST /auth/verify-otp` - Verificar código OTP y obtener JWT
- `POST /auth/forgot-password` - Solicitar token para resetear contraseña
- `POST /auth/verify-reset-password-otp` - Verificar OTP de reseteo
- `POST /auth/reset-password` - Resetear contraseña

### Gestión de Usuarios
- `GET /users` - Obtener todos los usuarios
- `GET /user/me` - Obtener usuario actual (requiere JWT)
- `GET /users/<user_id>` - Obtener usuario por ID
- `POST /user_registration` - Registrar nuevo usuario
- `PUT /user/<document_id>` - Actualizar usuario
- `DELETE /user/<document_id>?eliminate=true` - Eliminar usuario (soft delete)

### Gestión de Empresas
- `GET /companies` - Obtener todas las empresas
- `GET /companies/<id_company>` - Obtener empresa por ID

### Gestión de Sucursales
- `GET /branches` - Obtener todas las sucursales
- `GET /branches/<id_branch>` - Obtener sucursal por ID

### Gestión de Productos
- `GET /products` - Obtener todos los productos
- `GET /products/<id_product>` - Obtener producto por ID
- `POST /products` - Crear nuevo producto
- `PATCH /products/<id_product>` - Actualizar producto
- `DELETE /products/<id_product>` - Eliminar producto (soft delete)

### Gestión de Proveedores
- `GET /suppliers` - Obtener todos los proveedores
- `GET /suppliers/<id_supplier>` - Obtener proveedor por ID
- `POST /suppliers` - Crear nuevo proveedor
- `PATCH /suppliers/<id_supplier>` - Actualizar proveedor
- `DELETE /suppliers/<id_supplier>` - Eliminar proveedor (soft delete)

### Gestión de Inventarios
- `GET /inventories` - Obtener inventarios (con filtros opcionales)
- `GET /inventories/<id_inventory>` - Obtener inventario por ID

### Tipos de Transacciones
- `GET /transaction_types` - Obtener todos los tipos de transacción
- `GET /transaction_types/<id_transaction_type>` - Obtener tipo de transacción por ID

### Transacciones de Productos
- `GET /product-transactions` - Obtener todas las transacciones
- `GET /product-transactions/<id_product_transaction>` - Obtener transacción por ID
- `POST /product-transactions` - Crear nueva transacción
- `GET /product-transactions/report/excel` - Descargar reporte Excel de todas las transacciones

### Sistema de Logging
- `GET /logs` - Obtener todos los logs del sistema
- `GET /logs/<id_log>` - Obtener log específico

### Registros de Login
- `GET /user_logins` - Obtener todos los registros de login

## Flujo de Autenticación

### 1. Login Inicial
```json
POST /auth/login
{
  "username": "usuario",
  "password": "contraseña"
}
```

**Respuesta exitosa:**
```json
{
  "ok": true,
  "message": "Correo enviado exitosamente"
}
```

### 2. Verificación OTP
```json
POST /auth/verify-otp
{
  "username": "usuario",
  "token": "123456"
}
```

**Respuesta exitosa:**
```json
{
  "ok": true,
  "access_token": "jwt_token_aqui",
  "message": "Inicio de sesión exitoso",
  "username": "usuario",
  "name": "Nombre Completo",
  "role": 1,
  "branch_id": 1,
  "user_id": 1
}
```

### 3. Uso del JWT
Todas las peticiones protegidas requieren el JWT en el header:
```
Authorization: Bearer jwt_token_aqui
```

## Ejemplos de Uso

### Registro de Usuario
```json
POST /user_registration
{
  "name": "María González",
  "email": "maria.gonzalez@empresa.com",
  "username": "mgonzalez",
  "hashed_password": "password123",
  "document_id": "1234567890",
  "phone_number": "3001234567",
  "role_id": 2,
  "branch_id": 1
}
```

### Crear Producto
```json
POST /products
{
  "name": "Laptop Dell",
  "size": "15 pulgadas",
  "price": 2500000.00,
  "description": "Laptop para oficina con 8GB RAM"
}
```

### Crear Transacción de Producto
```json
POST /product-transactions
{
  "description": "Compra de laptops para oficina",
  "quantity": 5,
  "unit_price": 2500000.00,
  "transaction_date": "2024-01-15",
  "product_id": 1,
  "branch_id": 1,
  "transaction_type_id": 1,
  "app_user_id": 1,
  "supplier_id": 1
}
```

### Descargar Reporte Excel
```bash
GET /product-transactions/report/excel
Headers:
  Authorization: Bearer jwt_token_aqui
```

## Validaciones Implementadas

### Datos de Usuario
- **Email**: Formato válido de email
- **Teléfono**: Número colombiano válido (3XXXXXXXXX)
- **Documento**: Entre 6 y 10 dígitos
- **Unicidad**: Email, username y documento únicos en el sistema

### Datos de Proveedor
- **NIT**: Exactamente 9 dígitos
- **Teléfono**: Número colombiano válido
- **Email**: Formato válido de email
- **Nombres**: Mínimo 3 caracteres
- **Direcciones**: Mínimo 5 caracteres

### Datos de Producto
- **Nombre**: Mínimo 3 caracteres
- **Precio**: Mayor o igual a 0
- **Unicidad**: Nombre + tamaño únicos

### Datos de Transacción
- **Cantidad**: Mayor o igual a 0
- **Precio unitario**: Mayor o igual a 0
- **Descripción**: Mínimo 5 caracteres
- **Fecha**: Formato válido (DD/MM/YYYY o YYYY-MM-DD)

### Sistema de Tokens OTP
- **Expiración**: Tokens válidos por 10 minutos
- **Unicidad**: Cada token es único en el sistema
- **Uso único**: Los tokens se marcan como usados después de la verificación
- **Tipos**: OTP_LOGIN, RESET_PASSWORD

## Respuestas de la API

### Formato Estándar de Respuesta
```json
{
  "ok": true,
  "data": { ... },
  "message": "Operación exitosa"
}
```

### Formato de Error
```json
{
  "ok": false,
  "error": "Descripción del error"
}
```

## Códigos de Estado HTTP

- `200` - OK (Operación exitosa)
- `201` - Created (Recurso creado)
- `400` - Bad Request (Datos inválidos)
- `401` - Unauthorized (No autenticado o token expirado)
- `404` - Not Found (Recurso no encontrado)
- `500` - Internal Server Error (Error del servidor)

## Características Técnicas

### Sistema de JWT
- **Expiración**: 1 hora desde el login
- **Contenido**: user_id, username, role, is_active
- **Verificación**: Automática en endpoints protegidos
- **Secret Key**: Configurable mediante variable de entorno

### Sistema de Correo Electrónico
- **SMTP**: Configurado para Gmail
- **TLS**: Habilitado para conexión segura
- **Autenticación**: Contraseña de aplicación de Gmail
- **Manejo de errores**: Logging detallado de errores SMTP
- **Plantillas**: Correos personalizados para OTP y reseteo de contraseña

### Sistema de Tokens
- **Generación**: Tokens de 6 dígitos únicos
- **Expiración**: 10 minutos desde la creación
- **Tipos**: OTP_LOGIN, RESET_PASSWORD
- **Validación**: Verificación de expiración y uso

### Reportes Excel
- **Librería**: openpyxl 3.1.5
- **Formato**: Encabezados con estilo, columnas auto-ajustadas
- **Contenido**: Todas las transacciones con información completa
- **Descarga**: Automática mediante endpoint protegido

### Base de Datos
- **Soft Delete**: Implementado en todas las entidades
- **Timestamps**: created_at, updated_at, deleted_at
- **Relaciones**: Foreign keys con integridad referencial
- **Índices**: Optimización de consultas frecuentes
- **Transacciones**: Rollback automático en errores

### Seguridad
- **JWT**: Tokens de acceso seguros con expiración de 1 hora
- **Hash de contraseñas**: Usando bcrypt
- **CORS**: Configurado para dominio específico (localhost:5173)
- **Validación**: Sanitización de datos de entrada
- **Logging**: Registro de errores y operaciones críticas

### Gestión de Inventario
- **Actualización automática**: Al crear transacciones de productos
- **Validación de stock**: Prevención de stock negativo
- **Trazabilidad**: Historial completo de movimientos
- **Por sucursal**: Control independiente por ubicación

## Desarrollo

### Patrón Arquitectónico: Service Layer Architecture

El backend implementa una arquitectura en 3 capas claramente separadas:

#### Capa 1: Routes (Controllers)
- **Responsabilidad**: Manejo de peticiones HTTP
- **Ubicación**: `app/routes/`
- **Función**:
  - Recibir requests
  - Validar formato HTTP
  - Llamar a la capa de servicios
  - Retornar respuestas JSON
- **NO contiene**: Lógica de negocio

#### Capa 2: Services (Business Logic)
- **Responsabilidad**: Lógica de negocio
- **Ubicación**: `app/services/`
- **Función**:
  - Validación de datos de negocio
  - Procesamiento y cálculos
  - Orquestación de operaciones
  - Transacciones de base de datos
  - Logging de operaciones
- **Independiente de HTTP**: Puede ser reutilizada

#### Capa 3: Models (Data Layer)
- **Responsabilidad**: Representación de datos
- **Ubicación**: `app/models/`
- **Función**:
  - Definir estructura de tablas (SQLAlchemy ORM)
  - Relaciones entre entidades
  - Métodos de serialización (to_dict)
- **NO contiene**: Lógica de negocio

### Flujo de una Petición

```
HTTP Request
    ↓
Routes (Controller)
    ↓ delega
Services (Business Logic)
    ↓ usa
Models (ORM)
    ↓ consulta
Database (MySQL)
    ↓ retorna
Models → Services → Routes → HTTP Response (JSON)
```

### Estructura de Servicios
Cada entidad tiene su propio servicio que maneja:
- Validación de datos
- Lógica de negocio
- Interacción con la base de datos
- Manejo de errores
- Logging de operaciones

### Validaciones
- Validaciones de tipo de datos
- Validaciones de formato con regex
- Validaciones de unicidad
- Validaciones de negocio específicas
- Validación de relaciones entre entidades

### Soft Delete
Todas las entidades implementan soft delete usando el campo `deleted_at`, permitiendo:
- Recuperar datos eliminados
- Mantener integridad referencial
- Auditoría completa de cambios
- Restauración de registros

### Sistema de Logging
- Registro automático de errores
- Trazabilidad de operaciones críticas
- Información detallada para debugging
- Módulo y función que generó el log

## Dependencias Principales

```
Flask==2.3.2
Flask-SQLAlchemy==3.0.5
python-dotenv==1.0.0
PyMySQL==1.1.0
Flask-JWT-Extended==4.5.3
Flask-CORS==4.0.0
Flask-Mail==0.9.1
bcrypt==4.0.1
openpyxl==3.1.5
```

## Solución de Problemas

### Error de conexión a MySQL
- Verificar que MySQL esté corriendo
- Verificar credenciales en `.env`
- Verificar que la base de datos exista

### Error de SMTP
- Verificar configuración de Gmail
- Verificar que la contraseña de aplicación sea correcta
- Verificar que la verificación en 2 pasos esté habilitada

### Error de JWT
- Verificar que JWT_SECRET_KEY esté configurado
- Verificar que el token no haya expirado (1 hora)
- Verificar formato del header Authorization

### Error en reportes Excel
- Verificar que openpyxl esté instalado
- Verificar permisos de escritura
- Verificar que existan transacciones en la base de datos

## Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

Para preguntas o soporte, contactar al equipo de desarrollo.

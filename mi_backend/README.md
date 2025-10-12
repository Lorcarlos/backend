# Sistema de Gestión de Inventario - Backend API

Sistema de gestión de inventario empresarial desarrollado con Flask, SQLAlchemy y MariaDB. Proporciona una API REST completa para la administración de productos, inventarios, transacciones, personal y autenticación con OTP por correo electrónico.

## Características Principales

### Arquitectura
- **Framework**: Flask 2.3.2
- **ORM**: SQLAlchemy 3.0.5
- **Base de Datos**: MariaDB con SQLAlchemy
- **Autenticación**: JWT (JSON Web Tokens) con OTP por correo
- **Correo Electrónico**: Flask-Mail con SMTP de Gmail
- **Validación**: Regex y validaciones personalizadas
- **Patrón**: MVC (Model-View-Controller)
- **CORS**: Configurado para integración con frontend

### Modelos de Base de Datos
- **AppUser**: Gestión de usuarios del sistema con roles y sucursales
- **Company**: Gestión de empresas
- **Branch**: Sucursales de las empresas
- **Product**: Catálogo de productos con precios y categorías
- **Supplier**: Proveedores con información de contacto
- **Inventory**: Control de inventario por sucursal
- **TransactionType**: Tipos de transacciones (entrada/salida)
- **ProductTransaction**: Transacciones de productos con historial
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
- **Manejo de errores** consistente
- **CORS configurado** para integración con frontend

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
│   │   ├── log/
│   │   └── rol/
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
│   │   ├── mail_sender.py   # Envío de correos
│   │   ├── tokenGenerator.py
│   │   ├── tokenType.py
│   │   └── validator.py
│   ├── smtp_config.py       # Configuración SMTP
│   ├── database.py          # Configuración de base de datos
│   └── __init__.py          # Inicialización de la aplicación
├── requirements.txt         # Dependencias del proyecto
├── run.py                   # Punto de entrada de la aplicación
└── README.md                # Documentación del proyecto
```

## Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- MySQL 5.7 o superior
- pip (gestor de paquetes de Python)
- Cuenta de Gmail con verificación en 2 pasos habilitada

### 1. Clonar el Repositorio
```bash
git clone <url-del-repositorio>
cd mi_backend
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
DATABASE_URI="mysql+pymysql://usuario:password@127.0.0.1/nombre_base_datos"

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
1. Crear la base de datos en MySQL
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

### Gestión de Usuarios
- `GET /users` - Obtener todos los usuarios
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
- `GET /product-transaction` - Obtener todas las transacciones
- `GET /product-transaction/<id_product_transaction>` - Obtener transacción por ID
- `POST /product-transaction` - Crear nueva transacción

### Sistema de Logging
- `GET /logs` - Obtener todos los logs del sistema
- `GET /logs/<id_log>` - Obtener log específico

### Registros de Login
- `GET /user_logins` - Obtener todos los registros de login

### Permisos
- `GET /permissions` - Obtener permisos del sistema

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
  "role": 1,
  "branch_id": 1
}
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
  "document_id": 1234567890,
  "phone_number": 3001234567,
  "role_id": 2,
  "branch_id": 1
}
```

### Crear Producto
```json
POST /products
{
  "name": "Laptop Dell Inspiron",
  "description": "Laptop para oficina con 8GB RAM",
  "category": "Electrónicos",
  "unit_price": 2500000.00,
  "stock_quantity": 10
}
```

### Crear Transacción de Producto
```json
POST /product-transaction
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

## Validaciones Implementadas

### Datos de Usuario
- **Email**: Formato válido de email
- **Teléfono**: Número colombiano válido (3XXXXXXXXX)
- **Documento**: Entre 6 y 10 dígitos
- **Unicidad**: Email y documento únicos en el sistema

### Datos de Proveedor
- **NIT**: Exactamente 9 dígitos
- **Teléfono**: Número colombiano válido
- **Email**: Formato válido de email
- **Nombres**: Mínimo 3 caracteres
- **Direcciones**: Mínimo 5 caracteres

### Sistema de Tokens OTP
- **Expiración**: Tokens válidos por 10 minutos
- **Unicidad**: Cada token es único en el sistema
- **Uso único**: Los tokens se marcan como usados después de la verificación

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
- `404` - Not Found (Recurso no encontrado)
- `500` - Internal Server Error (Error del servidor)

## Características Técnicas

### Sistema de Correo Electrónico
- **SMTP**: Configurado para Gmail
- **TLS**: Habilitado para conexión segura
- **Autenticación**: Contraseña de aplicación de Gmail
- **Manejo de errores**: Logging detallado de errores SMTP

### Sistema de Tokens
- **Generación**: Tokens de 6 dígitos únicos
- **Expiración**: 10 minutos desde la creación
- **Tipos**: OTP_LOGIN, RESET_PASSWORD
- **Validación**: Verificación de expiración y uso

### Base de Datos
- **Soft Delete**: Implementado en todas las entidades
- **Timestamps**: created_at, updated_at, deleted_at
- **Relaciones**: Foreign keys con integridad referencial
- **Índices**: Optimización de consultas frecuentes

### Seguridad
- **JWT**: Tokens de acceso seguros
- **Hash de contraseñas**: Usando werkzeug.security
- **CORS**: Configurado para dominio específico
- **Validación**: Sanitización de datos de entrada

## Desarrollo

### Estructura de Servicios
Cada entidad tiene su propio servicio que maneja:
- Validación de datos
- Lógica de negocio
- Interacción con la base de datos
- Manejo de errores

### Validaciones
- Validaciones de tipo de datos
- Validaciones de formato con regex
- Validaciones de unicidad
- Validaciones de negocio específicas

### Soft Delete
Todas las entidades implementan soft delete usando el campo `deleted_at`, permitiendo recuperar datos eliminados.

### Sistema de Logging
- Registro automático de errores
- Trazabilidad de operaciones críticas
- Información detallada para debugging

## Dependencias Principales

```
Flask==2.3.2
Flask-SQLAlchemy==3.0.5
Flask-Mail==0.9.1
Flask-JWT-Extended==4.5.3
Flask-CORS==4.0.0
PyMySQL==1.1.0
python-dotenv==1.0.0
bcrypt==4.0.1
```

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
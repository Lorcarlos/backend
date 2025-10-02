# Sistema de Gestión de Inventario - Backend API

Sistema de gestión de inventario empresarial desarrollado con Flask, SQLAlchemy y MySQL. Proporciona una API REST completa para la administración de productos, inventarios, transacciones y personal.

## Características Principales

### Arquitectura
- **Framework**: Flask 2.3.2
- **ORM**: SQLAlchemy 3.0.5
- **Base de Datos**: MySQL
- **Autenticación**: JWT (JSON Web Tokens)
- **Validación**: Regex y validaciones personalizadas
- **Patrón**: MVC (Model-View-Controller)

### Modelos de Base de Datos
- **AppUser**: Gestión de usuarios del sistema
- **Company**: Gestión de empresas
- **Branch**: Sucursales de las empresas
- **Product**: Catálogo de productos
- **Supplier**: Proveedores
- **Inventory**: Control de inventario por sucursal
- **TransactionType**: Tipos de transacciones
- **ProductTransaction**: Transacciones de productos

### Funcionalidades Implementadas
- CRUD completo para todas las entidades
- Soft delete implementado en todas las tablas
- Validación robusta de datos con expresiones regulares
- Autenticación y autorización con JWT
- Estructura MVC con separación clara de responsabilidades
- API REST con respuestas JSON estandarizadas
- Manejo de errores consistente
- CORS configurado para integración con frontend

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
│   │   └── staff/
│   ├── routes/              # Endpoints de la API
│   │   ├── company/
│   │   ├── branch/
│   │   ├── product/
│   │   ├── supplier/
│   │   ├── inventory/
│   │   ├── transaction_type/
│   │   ├── product_transaction/
│   │   ├── staff/
│   │   └── login/
│   ├── services/            # Lógica de negocio
│   │   ├── company/
│   │   ├── branch/
│   │   ├── product/
│   │   ├── supplier/
│   │   ├── inventory/
│   │   ├── transaction_type/
│   │   ├── product_transaction/
│   │   └── staff/
│   ├── validator/           # Validaciones de datos
│   ├── utils/              # Utilidades y helpers
│   └── database.py         # Configuración de base de datos
├── instance/               # Archivos de instancia
├── tests/                  # Pruebas unitarias
├── requirements.txt        # Dependencias del proyecto
├── run.py                 # Punto de entrada de la aplicación
└── README.md              # Documentación del proyecto
```

## Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- MySQL 5.7 o superior
- pip (gestor de paquetes de Python)

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
DATABASE_URI=mysql://usuario:password@localhost:3306/nombre_base_datos
JWT_SECRET_KEY=tu_clave_secreta_jwt
```

### 5. Configurar Base de Datos
1. Crear la base de datos en MySQL
2. Ejecutar la aplicación para crear las tablas automáticamente:
```bash
python run.py
```

### 6. Ejecutar la Aplicación
```bash
python run.py
```

La aplicación estará disponible en `http://localhost:5000`

## API Endpoints

### Autenticación
- `POST /auth/login` - Iniciar sesión

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

### Permisos
- `GET /permissions` - Obtener permisos del sistema

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


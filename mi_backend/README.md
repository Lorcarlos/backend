# Sistema de Inventario Flask

Sistema de gestión de inventario desarrollado con Flask y SQLAlchemy.

## Características Implementadas

### Modelos de Base de Datos
- **Company**: Gestión de empresas
- **Branch**: Sucursales de las empresas
- **Product**: Catálogo de productos
- **Supplier**: Proveedores
- **Inventory**: Control de inventario por sucursal
- **Transaction_type**: Tipos de transacciones

### Funcionalidades
- CRUD completo para todas las entidades
- Soft delete implementado
- Validación de datos con regex
- Estructura MVC con separación de responsabilidades
- API REST con respuestas JSON estandarizadas

### Estructura del Proyecto
```
app/
├── models/          # Modelos de SQLAlchemy
├── routes/          # Endpoints de la API
├── services/        # Lógica de negocio
├── validator/       # Validaciones de datos
└── const/           # Constantes y consultas
```

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
python -m pip install python-dotenv

```

2. Configurar variables de entorno:
Crear archivo `.env` con:
```
DATABASE_URI=mysql://usuario:password@localhost/nombre_bd
```

3. Ejecutar la aplicación:
```bash
python run.py
```

## Endpoints Disponibles

- `/products` - Gestión de productos
- `/suppliers` - Gestión de proveedores
- `/companies` - Gestión de empresas
- `/branches` - Gestión de sucursales
- `/inventories` - Consulta de inventarios
- `/transaction_types` - Tipos de transacciones
- `/users` -get  se lectura para ver usuarios
- `/user_registration` - registro de personal
- `/user_registration` - registro de personal
-  `/user/987654321?eliminate=true` -eliminar usuarios
-`/user/1472583691` - put

json
{
  "name": "María González",
  "email": "asdriaada@example.com",
  "username": "adapa",
  "hashed_password": "securepass123",
  "document_id":1472583671,
  "phone_number":3234567891,
  "role_id": 2,
  "branch_id": 3
}


from ...models.supplier.supplier import Supplier
from ...utils.validator import validate_data, validate_supplier_data
from ...utils.soft_delete_handler import SoftDeleteHandler
from ...services.log.log_service import LogService
from ...database import db
from datetime import datetime, timezone


class SupplierService:

    @staticmethod
    def get_all_suppliers() -> list[dict]:

        suppliers = Supplier.query.filter(Supplier.deleted_at.is_(None)).all()

        return [supplier.to_dict() for supplier in suppliers]

    @staticmethod
    def get_supplier_by_id(id_supplier):

        supplier = Supplier.query.filter(
            Supplier.deleted_at.is_(None), Supplier.id == id_supplier
        ).first()

        if supplier is None:
            LogService.create_log(
                {
                    "module": f"{SupplierService.__name__}.{SupplierService.get_supplier_by_id.__name__}",
                    "message": "No se encontró el proveedor buscado por id",
                }
            )
            raise ValueError("El proveedor no se encontró")

        return supplier

    @staticmethod
    def create_supplier(supplier):

        required_fields = {
            "name": str,
            "nit": str,
            "email": str,
            "contact_name": str,
            "phone_number": str,
            "address": str,
            "city": str,
            "description": str,
        }

        validate_data(supplier, required_fields)

        supplier["name"] = supplier["name"].strip().lower()
        supplier["email"] = supplier["email"].strip().lower()
        supplier["contact_name"] = supplier["contact_name"].strip().lower()
        supplier["address"] = supplier["address"].strip()
        supplier["city"] = supplier["city"].strip().lower()

        validate_supplier_data(supplier)

        # Llama al handler que verifica si el elemento existe y está activo o si existe y está soft_deleted
        return SoftDeleteHandler.create_or_restore(
            model=Supplier,
            unique_filters=Supplier.nit == supplier["nit"],
            data=supplier,
            restore_fn=SupplierService.restore_deleted_supplier,
            create_fn=SupplierService.create_fresh_supplier,
        )

    @staticmethod
    def update_supplier_by_id(id_supplier, data):

        supplier = SupplierService.get_supplier_by_id(id_supplier)

        allowed_fields = [
            "name",
            "nit",
            "email",
            "contact_name",
            "phone_number",
            "address",
            "city",
            "description",
            "is_active",
        ]

        validate_supplier_data(data)

        for key, value in data.items():
            if key not in allowed_fields:
                LogService.create_log(
                    {
                        "module": f"{SupplierService.__name__}.{SupplierService.update_supplier_by_id.__name__}",
                        "message": f"Se intentó actualizar {key} del proveedor, lo cual no está permitido",
                    }
                )
                raise ValueError("Se intentó actualizar un campo inválido")

            setattr(supplier, key, value)

        supplier_exists = Supplier.query.filter(
            Supplier.deleted_at.is_(None),
            Supplier.id != supplier.id,
            Supplier.nit == supplier.nit,
        ).first()

        if supplier_exists:
            LogService.create_log(
                {
                    "module": f"{SupplierService.__name__}.{SupplierService.update_supplier_by_id.__name__}",
                    "message": "Se intentó actualizar el nit de un proveedor a uno que ya existe",
                }
            )
            raise ValueError("Ya existe otro proveedor con el mismo nit")

        db.session.commit()

        return supplier

    @staticmethod
    def deleted_supplier_by_id(id_supplier):

        supplier = SupplierService.get_supplier_by_id(id_supplier)

        supplier.deleted_at = datetime.now(timezone.utc)

        db.session.commit()

        return True

    @staticmethod
    def restore_deleted_supplier(
        existing_supplier: Supplier, new_data: dict
    ) -> Supplier:
        """Restaura proveedor eliminado actualizando todos los campos pero manteniendo created_at original"""
        # Actualizar todos los campos de datos
        existing_supplier.name = new_data["name"].strip().lower()
        existing_supplier.nit = new_data["nit"]
        existing_supplier.email = new_data["email"].strip().lower()
        existing_supplier.contact_name = new_data["contact_name"].strip().lower()
        existing_supplier.phone_number = new_data["phone_number"]
        existing_supplier.address = new_data["address"].strip()
        existing_supplier.city = new_data["city"].strip().lower()
        existing_supplier.description = new_data["description"]
        existing_supplier.is_active = new_data.get("is_active", True)

        # Solo actualizar updated_at y limpiar deleted_at
        existing_supplier.updated_at = datetime.now(timezone.utc)
        existing_supplier.deleted_at = None
        # created_at se mantiene igual (cuándo se creó originalmente)

        db.session.commit()
        return existing_supplier

    @staticmethod
    def create_fresh_supplier(supplier_data: dict) -> Supplier:
        """Crea un proveedor completamente nuevo"""
        new_supplier = Supplier(
            name=supplier_data["name"],
            nit=supplier_data["nit"],
            email=supplier_data["email"],
            contact_name=supplier_data["contact_name"],
            phone_number=supplier_data["phone_number"],
            address=supplier_data["address"],
            city=supplier_data["city"],
            description=supplier_data["description"],
            is_active=supplier_data.get("is_active", True),
        )

        db.session.add(new_supplier)
        db.session.commit()

        return new_supplier

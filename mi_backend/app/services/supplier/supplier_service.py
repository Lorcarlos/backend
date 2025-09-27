from ...models.supplier.supplier import Supplier
from ...validator.validator import validate_data, validate_supplier_data
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
            "description": str,
        }

        validate_data(supplier, required_fields)

        supplier["name"] = supplier["name"].strip().lower()
        supplier["email"] = supplier["email"].strip().lower()
        supplier["contact_name"] = supplier["contact_name"].strip().lower()
        supplier["address"] = supplier["address"].strip()

        validate_supplier_data(supplier)

        supplier_exists = Supplier.query.filter(
            Supplier.deleted_at.is_(None), Supplier.nit == supplier["nit"]
        ).first()

        if supplier_exists:
            raise ValueError("El proveedor ya existe")

        new_supplier = Supplier(
            name=supplier["name"],
            nit=supplier["nit"],
            email=supplier["email"],
            contact_name=supplier["contact_name"],
            phone_number=supplier["phone_number"],
            address=supplier["address"],
            description=supplier["description"],
            is_active=supplier.get("is_active", True),
        )

        db.session.add(new_supplier)
        db.session.commit()

        return new_supplier

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
            "description",
            "is_active",
        ]

        validate_supplier_data(data)
        
        for key, value in data.items():
            if key not in allowed_fields:
                raise ValueError("Se intentó actualizar un campo inválido")

            setattr(supplier, key, value)


        supplier_exists = Supplier.query.filter(
            Supplier.deleted_at.is_(None),
            Supplier.id != supplier.id,
            Supplier.nit == supplier.nit,
        ).first()

        if supplier_exists:
            raise ValueError("Ya existe otro proveedor con el mismo nit")

        db.session.commit()

        return supplier

    @staticmethod
    def deleted_supplier_by_id(id_supplier):

        supplier = SupplierService.get_supplier_by_id(id_supplier)

        supplier.deleted_at = datetime.now(timezone.utc)

        db.session.commit()

        return True

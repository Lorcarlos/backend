# Importar todos los modelos para que SQLAlchemy los reconozca
from .company.company import Company
from .branch.branch import Branch
from .product.product import Product
from .supplier.supplier import Supplier
from .inventory.inventory import Inventory
from .transaction_type.transaction_type import TransactionType
from .product_transaction.product_transaction import ProductTransaction
from .staff.staff_peticion import AppUser

# Exportar todos los modelos para facilitar las importaciones
__all__ = [
    'Company',
    'Branch', 
    'Product',
    'Supplier',
    'Inventory',
    'TransactionType',
    'ProductTransaction',
    'AppUser'
]

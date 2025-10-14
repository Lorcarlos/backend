from ...database import db
from datetime import datetime, timezone


class ProductTransaction(db.Model):
    __tablename__ = "product_transaction"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(15, 2), nullable=False)
    total_price = db.Column(db.Numeric(15, 2), nullable=False)
    transaction_date = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey("supplier.id"), nullable=True)
    branch_id = db.Column(db.Integer, db.ForeignKey("branch.id"), nullable=False)
    transaction_type_id = db.Column(
        db.Integer, db.ForeignKey("transaction_type.id"), nullable=False
    )
    app_user_id = db.Column(db.Integer, db.ForeignKey("app_user.id"), nullable=False)

    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    product = db.relationship("Product", backref="product_transactions")
    supplier = db.relationship("Supplier", backref="product_transactions")
    branch = db.relationship("Branch", backref="product_transactions")
    transaction_type = db.relationship(
        "TransactionType", backref="product_transactions"
    )
    app_user = db.relationship("AppUser", backref="product_transactions")

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "quantity": float(self.quantity) if self.quantity is not None else None,
            "unit_price": (
                float(self.unit_price) if self.unit_price is not None else None
            ),
            "total_price": (
                float(self.total_price) if self.total_price is not None else None
            ),
            "transaction_date": self.transaction_date,
            "product": f"{self.product.name} {self.product.size}",
            "supplier_name": self.supplier.name if self.supplier else None,
            "branch_name": self.branch.name,
            "transaction_type_name": self.transaction_type.name,
            "app_user_name": self.app_user.name,
            "created_at": self.created_at,
        }

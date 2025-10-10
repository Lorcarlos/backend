from ...database import db
from datetime import datetime, timezone


class Inventory(db.Model):
    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey("branch.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    deleted_at = db.Column(db.DateTime, nullable=True)

    product = db.relationship("Product", backref="inventories")
    branch = db.relationship("Branch", backref="inventories")

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_name": self.product.name if self.product else None,
            "price":self.product.price if self.product else None,
            "product_size": self.product.size if self.product else None,
            "branch_id": self.branch_id,
            "quantity": float(self.quantity) if self.quantity is not None else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

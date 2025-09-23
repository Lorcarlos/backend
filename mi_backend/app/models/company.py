from ..database import db
from datetime import datetime, timezone


class Company(db.Model):
    __tablename__ = "company"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    nit = db.Column(db.String(20), nullable=False, unique=True)

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

    # Índice para acelerar consultas
    __table_args__ = (db.UniqueConstraint("nit", name="uq_company_nit"),)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "nit": self.nit,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }

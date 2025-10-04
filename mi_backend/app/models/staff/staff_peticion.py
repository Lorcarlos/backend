from datetime import datetime, timezone
from ...database import db


class AppUser(db.Model):
    __tablename__ = "app_user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    document_id = db.Column(db.BigInteger, unique=True, nullable=False)
    phone_number = db.Column(db.BigInteger, nullable=False)
    role_id = db.Column(db.Integer, nullable=False, default=1)
    branch_id = db.Column(db.Integer, db.ForeignKey("branch.id"), nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    
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

    def __repr__(self):
        return f"<AppUser {self.username} - Role_id: {self.role_id}>"

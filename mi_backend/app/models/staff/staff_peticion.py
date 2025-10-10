from datetime import datetime, timezone
from ...database import db


class AppUser(db.Model):
    __tablename__ = "app_user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    document_id = db.Column(db.BigInteger, unique=False, nullable=True)
    phone_number = db.Column(db.BigInteger, nullable=True)
    role_id = db.Column(db.Integer, nullable=False, default=1)
    branch_id = db.Column(db.Integer, db.ForeignKey("branch.id"), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    __table_args__ = (
        db.UniqueConstraint('document_id', 'deleted_at', 
                            name='uq_document_id_active'),
        db.UniqueConstraint('username', 'deleted_at', 
                            name='uq_username_active'),
    )

    def __repr__(self):
        return f"<AppUser {self.username} - Role_id: {self.role_id}>"
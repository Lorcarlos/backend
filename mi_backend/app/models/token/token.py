from ...database import db
from datetime import datetime, timezone


class Token(db.Model):
    __tablename__ = "token"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(6), nullable=False)
    app_user_id = db.Column(db.Integer, db.ForeignKey("app_user.id"), nullable=False)
    type = db.Column(
        db.Enum("OTP_LOGIN", "RESET_PASSWORD", name="token_type"), nullable=False
    )
    is_used = db.Column(db.Boolean, nullable=False, default=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    app_user = db.relationship("AppUser", backref="tokens")

    def to_dict(self):

        return {
            "id": self.id,
            "token": self.token,
            "app_user_id": self.app_user_id,
            "type": self.type,
            "is_used": self.is_used,
            "expires_at": self.expires_at,
            "created_at": self.created_at,
        }

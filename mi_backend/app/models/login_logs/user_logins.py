from ...database import db
from datetime import datetime, timezone


class UserLogins(db.Model):
    __tablename__ = "user_logins"

    id = db.Column(db.Integer, primary_key=True)
    app_user_id = db.Column(db.Integer, db.ForeignKey("app_user.id"), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    app_user = db.relationship("AppUser", backref="user_logins")

    def to_dict(self):
        return {
            "id": self.id,
            "app_user_id": self.app_user_id,
            "app_user_username ": self.app_user.username,
            "app_user_email ": self.app_user.email,
            "created_at": self.created_at,
        }

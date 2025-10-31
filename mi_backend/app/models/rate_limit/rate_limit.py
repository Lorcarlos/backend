from ...database import db
from datetime import datetime, timedelta


class RateLimit(db.Model):
    __tablename__ = "rate_limit"

    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(255), nullable=False, index=True)  # username, email, or IP
    endpoint = db.Column(db.String(100), nullable=False, index=True)  # login, verify-otp, etc.
    attempts = db.Column(db.Integer, default=0, nullable=False)
    last_attempt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    blocked_until = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<RateLimit {self.identifier} - {self.endpoint} - {self.attempts} attempts>"

    @staticmethod
    def is_blocked(identifier, endpoint):
        """Check if identifier is currently blocked for this endpoint"""
        record = RateLimit.query.filter_by(
            identifier=identifier,
            endpoint=endpoint
        ).first()

        if not record:
            return False

        if record.blocked_until and datetime.utcnow() < record.blocked_until:
            return True

        return False

    @staticmethod
    def get_remaining_attempts(identifier, endpoint, max_attempts=5):
        """Get remaining attempts before blocking"""
        record = RateLimit.query.filter_by(
            identifier=identifier,
            endpoint=endpoint
        ).first()

        if not record:
            return max_attempts

        # Reset if last attempt was more than 15 minutes ago
        if datetime.utcnow() - record.last_attempt > timedelta(minutes=15):
            record.attempts = 0
            record.blocked_until = None
            db.session.commit()
            return max_attempts

        return max(0, max_attempts - record.attempts)

    @staticmethod
    def record_attempt(identifier, endpoint, max_attempts=5, block_duration_minutes=30):
        """
        Record a failed attempt and block if max attempts exceeded

        Args:
            identifier: username, email, or IP address
            endpoint: the endpoint being accessed
            max_attempts: maximum attempts before blocking (default 5)
            block_duration_minutes: how long to block after max attempts (default 30)

        Returns:
            tuple: (remaining_attempts, is_now_blocked, time_until_unblock)
        """
        record = RateLimit.query.filter_by(
            identifier=identifier,
            endpoint=endpoint
        ).first()

        current_time = datetime.utcnow()

        if not record:
            record = RateLimit(
                identifier=identifier,
                endpoint=endpoint,
                attempts=1,
                last_attempt=current_time
            )
            db.session.add(record)
        else:
            # Reset if last attempt was more than 15 minutes ago
            if current_time - record.last_attempt > timedelta(minutes=15):
                record.attempts = 1
                record.blocked_until = None
            else:
                record.attempts += 1

            record.last_attempt = current_time

        # Block if max attempts exceeded
        if record.attempts >= max_attempts:
            record.blocked_until = current_time + timedelta(minutes=block_duration_minutes)
            db.session.commit()
            return (0, True, record.blocked_until)

        db.session.commit()
        remaining = max_attempts - record.attempts
        return (remaining, False, None)

    @staticmethod
    def reset_attempts(identifier, endpoint):
        """Reset attempts for successful authentication"""
        record = RateLimit.query.filter_by(
            identifier=identifier,
            endpoint=endpoint
        ).first()

        if record:
            record.attempts = 0
            record.blocked_until = None
            db.session.commit()

    @staticmethod
    def get_block_time_remaining(identifier, endpoint):
        """Get remaining block time in minutes"""
        record = RateLimit.query.filter_by(
            identifier=identifier,
            endpoint=endpoint
        ).first()

        if not record or not record.blocked_until:
            return 0

        if datetime.utcnow() >= record.blocked_until:
            return 0

        time_diff = record.blocked_until - datetime.utcnow()
        return int(time_diff.total_seconds() / 60)

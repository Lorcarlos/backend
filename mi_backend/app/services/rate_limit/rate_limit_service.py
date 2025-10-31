from ...models.rate_limit.rate_limit import RateLimit
from ...database import db


class RateLimitService:
    """Service for managing rate limiting across the application"""

    # Rate limit configurations
    RATE_LIMITS = {
        "login": {
            "max_attempts": 5,
            "block_duration_minutes": 30,
            "reset_window_minutes": 15
        },
        "verify-otp": {
            "max_attempts": 3,
            "block_duration_minutes": 15,
            "reset_window_minutes": 15
        },
        "verify-otp-password": {
            "max_attempts": 3,
            "block_duration_minutes": 15,
            "reset_window_minutes": 15
        },
        "forgot-password": {
            "max_attempts": 5,
            "block_duration_minutes": 30,
            "reset_window_minutes": 15
        }
    }

    @staticmethod
    def check_and_record_attempt(identifier, endpoint):
        """
        Check if blocked and record attempt if not

        Returns:
            dict: {
                "is_blocked": bool,
                "remaining_attempts": int,
                "block_time_remaining": int (minutes),
                "message": str
            }
        """
        config = RateLimitService.RATE_LIMITS.get(endpoint, {
            "max_attempts": 5,
            "block_duration_minutes": 30
        })

        # Check if already blocked
        if RateLimit.is_blocked(identifier, endpoint):
            remaining_time = RateLimit.get_block_time_remaining(identifier, endpoint)
            return {
                "is_blocked": True,
                "remaining_attempts": 0,
                "block_time_remaining": remaining_time,
                "message": f"Cuenta bloqueada temporalmente. Intenta nuevamente en {remaining_time} minutos"
            }

        # Record the failed attempt
        remaining, is_blocked, block_until = RateLimit.record_attempt(
            identifier,
            endpoint,
            max_attempts=config["max_attempts"],
            block_duration_minutes=config["block_duration_minutes"]
        )

        if is_blocked:
            block_time = config["block_duration_minutes"]
            return {
                "is_blocked": True,
                "remaining_attempts": 0,
                "block_time_remaining": block_time,
                "message": f"Demasiados intentos fallidos. Cuenta bloqueada por {block_time} minutos"
            }

        return {
            "is_blocked": False,
            "remaining_attempts": remaining,
            "block_time_remaining": 0,
            "message": f"Intento fallido. Te quedan {remaining} intentos"
        }

    @staticmethod
    def is_blocked(identifier, endpoint):
        """Check if identifier is blocked for endpoint"""
        return RateLimit.is_blocked(identifier, endpoint)

    @staticmethod
    def reset(identifier, endpoint):
        """Reset rate limit for successful authentication"""
        RateLimit.reset_attempts(identifier, endpoint)

    @staticmethod
    def get_status(identifier, endpoint):
        """
        Get current rate limit status

        Returns:
            dict: Current status information
        """
        config = RateLimitService.RATE_LIMITS.get(endpoint, {
            "max_attempts": 5,
            "block_duration_minutes": 30
        })

        is_blocked = RateLimit.is_blocked(identifier, endpoint)
        remaining = RateLimit.get_remaining_attempts(
            identifier,
            endpoint,
            max_attempts=config["max_attempts"]
        )
        block_time = RateLimit.get_block_time_remaining(identifier, endpoint)

        return {
            "is_blocked": is_blocked,
            "remaining_attempts": remaining,
            "block_time_remaining": block_time,
            "max_attempts": config["max_attempts"]
        }

    @staticmethod
    def clear_all_for_identifier(identifier):
        """Clear all rate limit records for an identifier (admin function)"""
        records = RateLimit.query.filter_by(identifier=identifier).all()
        for record in records:
            db.session.delete(record)
        db.session.commit()
        return len(records)

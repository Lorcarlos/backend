from ...database import db

class Login(db.Model):
    __tablename__ = "Login"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Login {self.username}>"

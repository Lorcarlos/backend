
from .. import db

class Material(db.Model):
    __tablename__ = 'Materials'  # ¡El nombre exacto de la tabla en la base!

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    quantuty = db.Column(db.Integer)
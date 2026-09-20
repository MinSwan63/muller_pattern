from datetime import datetime
from app import db


class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    calculations = db.relationship(
        "Calculation",
        backref="client",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="Calculation.created_at.desc()",
    )

    def latest_measurements(self):
        last = (
            Calculation.query.filter_by(client_id=self.id)
            .order_by(Calculation.created_at.desc())
            .first()
        )
        return last.measurements if last else {}

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone or "",
            "notes": self.notes or "",
        }

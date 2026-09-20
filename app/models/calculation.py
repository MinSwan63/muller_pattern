import json
from datetime import datetime
from app import db


class Calculation(db.Model):
    __tablename__ = "calculations"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=True)
    pattern = db.Column(db.String(50), nullable=False)
    measurements_json = db.Column(db.Text, nullable=False, default="{}")
    results_json = db.Column(db.Text, nullable=False, default="{}")
    unit = db.Column(db.String(10), nullable=False, default="cm")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def measurements(self):
        try:
            return json.loads(self.measurements_json or "{}")
        except json.JSONDecodeError:
            return {}

    @measurements.setter
    def measurements(self, value):
        self.measurements_json = json.dumps(value, ensure_ascii=False)

    @property
    def results(self):
        try:
            return json.loads(self.results_json or "{}")
        except json.JSONDecodeError:
            return {}

    @results.setter
    def results(self, value):
        self.results_json = json.dumps(value, ensure_ascii=False)

import json
from datetime import datetime
from app import db

class RCAReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    report_data = db.Column(db.Text, nullable=False)  # stored as a JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        data = json.loads(self.report_data)
        data.update({'id': self.id, 'title': self.title, 'created_at': self.created_at.strftime("%Y-%m-%d %H:%M")})
        return data


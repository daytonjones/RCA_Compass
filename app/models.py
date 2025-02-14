# app/models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class RCAReport(db.Model):
    __tablename__ = 'rca_reports'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    issue_description = db.Column(db.Text)
    incident_date = db.Column(db.String(50))
    incident_description = db.Column(db.Text)
    who_reported = db.Column(db.String(255))
    who_affected = db.Column(db.String(255))
    how_affected = db.Column(db.Text)
    how_often = db.Column(db.String(255))
    events_before = db.Column(db.Text)
    events_during = db.Column(db.Text)
    events_after = db.Column(db.Text)
    staff_involved = db.Column(db.Text)
    job_titles = db.Column(db.Text)
    data_collection_methods = db.Column(db.Text)
    communication_plan = db.Column(db.Text)
    root_cause = db.Column(db.Text)
    cause_occurrence = db.Column(db.Text)
    supporting_data = db.Column(db.Text)
    resolution_steps = db.Column(db.Text)
    date_resolved = db.Column(db.String(50))
    approved_by = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def init_db():
    db.create_all()


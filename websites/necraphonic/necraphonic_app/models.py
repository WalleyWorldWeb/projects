from . import db
from datetime import datetime

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    venue = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100)) # Optional
    ticket_url = db.Column(db.String(255))
    details = db.Column(db.Text) # e.g., 'With special guests...'

    def __repr__(self):
        return f'<Show {self.venue} on {self.date.strftime("%Y-%m-%d")}>'

# You could add models for Members, Tracks, Videos later
# class Member(db.Model): ...
# class Track(db.Model): ...
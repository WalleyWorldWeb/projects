from flask import Blueprint, render_template
from ..models import Show
from datetime import datetime

shows_bp = Blueprint('shows', __name__)

@shows_bp.route('/')
def list_shows():
    today = datetime.utcnow()
    # Query upcoming shows, ordered by date
    upcoming_shows = Show.query.filter(Show.date >= today)\
                               .order_by(Show.date.asc()).all()
    # Optional: Query past shows
    past_shows = Show.query.filter(Show.date < today)\
                           .order_by(Show.date.desc()).limit(10).all() # Example: limit past shows

    return render_template('shows.html',
                           title="Shows",
                           upcoming_shows=upcoming_shows,
                           past_shows=past_shows)
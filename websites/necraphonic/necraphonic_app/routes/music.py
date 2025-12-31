# necraphonic_app/routes/music.py

from flask import Blueprint, render_template # Add other imports as needed

# DEFINE THE BLUEPRINT - Ensure the name is exactly 'music_bp'
music_bp = Blueprint('music', __name__, template_folder='../templates')

# --- Define Routes for the Music Section ---

@music_bp.route('/') # Corresponds to the '/music/' URL prefix defined in __init__.py
def music_home():
    # Add logic for your main music/video essay page here
    return render_template('music.html', title="Music") # Make sure music.html exists

# Add other routes related to music here
# e.g., @music_bp.route('/track/<track_id>')
#      def track_details(track_id): ...
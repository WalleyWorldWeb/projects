# necraphonic_app/routes/main.py

from flask import Blueprint, render_template # Add other imports like request, redirect, url_for as needed

# DEFINE THE BLUEPRINT - Make sure the name is exactly 'main_bp'
main_bp = Blueprint('main', __name__, template_folder='../templates') # You can adjust template_folder if needed

# --- Define Routes using this Blueprint ---

@main_bp.route('/') # Route for the homepage
def home():
    # Add logic for your homepage here
    return render_template('index.html', title="Home") # Make sure index.html exists

@main_bp.route('/contact') # Example route for contact page
def contact():
    # Add logic for contact page if handled here, or create contact_bp later
    return render_template('contact.html', title="Contact") # Make sure contact.html exists

# Add other main routes here (e.g., about page)
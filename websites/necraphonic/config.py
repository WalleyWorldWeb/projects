import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-should-really-change-this'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Add other configurations like Flask-Mail settings here
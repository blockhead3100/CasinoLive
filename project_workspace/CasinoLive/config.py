from flask import Flask
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback_secret_key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///casino.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_USERNAME = 'admin'  # Set the admin username
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin_password')  # Set the admin password

app = Flask(__name__)
app.config.from_object(Config)
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import requests
from models import db, Instagram
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import settings

# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)
# Configure the database URI for SQLite
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = settings.PostgreSQL_Connection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)

# Create the database and tables if they do not exist
with app.app_context():
    db.create_all()


"""
########################Below commands to run this file########################
# Generate migration script
python manage.py db migrate

# Apply migrations 
python db upgrade
"""

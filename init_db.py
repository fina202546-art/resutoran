from app import app
from extensions import db

from models import Contact, Reservation

with app.app_context():
    print("Creating tables...")
    db.create_all()
    print("Done!")

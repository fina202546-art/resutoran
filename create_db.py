from app import app
from extensions import db
from models import Reservation, Contact

with app.app_context():
    db.create_all()
    print("Tables created!")

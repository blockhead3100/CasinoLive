from app import db, User
from models import app
from werkzeug.security import generate_password_hash

if __name__ == '__main__':
    with app.app_context():  # Ensure the app context is active
        db.create_all()  # Create database tables only if they don't exist

        # Add initial users
        admin = User(username="admin", password=generate_password_hash("admin123"), balance=1000.0)
        db.session.add(admin)
        db.session.commit()

    print("Database initialized successfully!")
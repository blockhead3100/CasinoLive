from models import db, app

if __name__ == '__main__':
    with app.app_context():  # Ensure the app context is active
        db.create_all()  # Create database tables only if they don't exist
    print("Database initialized successfully!")
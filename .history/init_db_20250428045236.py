from app import db, User
from models import app
from werkzeug.security import generate_password_hash

def add_admin_account():
    admin_username = "admin"
    admin_password = "admin"  # Replace with a secure password in production

    # Check if admin account already exists
    existing_admin = User.query.filter_by(username=admin_username).first()
    if not existing_admin:
        admin_user = User(username=admin_username, password=generate_password_hash(admin_password), is_admin=True)
        db.session.add(admin_user)
        db.session.commit()
        print("Admin account created successfully.")
    else:
        print("Admin account already exists.")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure the database schema is up-to-date
        add_admin_account()

    print("Database initialized successfully!")
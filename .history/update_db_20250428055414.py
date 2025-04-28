from app import db

def add_is_admin_column():
    with db.engine.connect() as connection:
        connection.execute("ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT FALSE")

if __name__ == "__main__":
    add_is_admin_column()
    print("is_admin column added successfully.")
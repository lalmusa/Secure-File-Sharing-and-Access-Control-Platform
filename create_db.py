print("Starting create_db.py")

from app import create_app, db

print("Imports successful")

app = create_app()

print("App created")

with app.app_context():
    print("Inside app context")
    db.create_all()
    print("Database created successfully")
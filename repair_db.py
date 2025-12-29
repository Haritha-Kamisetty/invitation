from app import create_app, db
from app.models import User, Event
import os

# Ensure DB file is gone
if os.path.exists('invitation.db'):
    try:
        os.remove('invitation.db')
        print("Deleted existing invitation.db")
    except Exception as e:
        print(f"Error deleting invitation.db: {e}")

app = create_app()
with app.app_context():
    try:
        # Force create all tables
        db.create_all()
        print("Database tables created successfully")
        
        # Verify schema
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        columns = [c['name'] for c in inspector.get_columns('event')]
        print(f"Event table columns: {columns}")
        
        if 'user_id' in columns:
            print("SUCCESS: user_id column exists in Event table")
        else:
            print("FAILURE: user_id column MISSING from Event table")
            
    except Exception as e:
        print(f"Error during DB initialization: {e}")

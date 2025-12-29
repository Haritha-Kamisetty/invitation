import os
from app import create_app, db
from sqlalchemy import inspect

# Delete the database file completely
if os.path.exists('invitation.db'):
    os.remove('invitation.db')
    print("Deleted old database file")

app = create_app()
with app.app_context():
    # Drop all tables first (in case db file exists)
    db.drop_all()
    print("Dropped all tables")
    
    # Create all tables fresh
    db.create_all()
    print("Created all tables fresh")
    
    # Verify the schema
    inspector = inspect(db.engine)
    event_columns = [c['name'] for c in inspector.get_columns('event')]
    user_columns = [c['name'] for c in inspector.get_columns('user')]
    
    print(f"\nUser table columns: {user_columns}")
    print(f"Event table columns: {event_columns}")
    
    if 'user_id' in event_columns:
        print("\n✓ SUCCESS: Database schema is correct!")
    else:
        print("\n✗ FAILURE: user_id column still missing!")

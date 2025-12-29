import sys
import os

# Remove all cached modules
for module in list(sys.modules.keys()):
    if 'app' in module:
        del sys.modules[module]

# Delete database file
if os.path.exists('invitation.db'):
    os.remove('invitation.db')
    print("Deleted invitation.db")

# Now import fresh
from app import create_app, db
from app.models import Event
from sqlalchemy import inspect

app = create_app()
with app.app_context():
    # Check what SQLAlchemy thinks the model looks like
    print("\nEvent model columns from SQLAlchemy:")
    for column in Event.__table__.columns:
        print(f"  - {column.name}: {column.type}")
    
    # Create tables
    db.create_all()
    print("\nDatabase created")
    
    # Verify what was actually created
    inspector = inspect(db.engine)
    columns = inspector.get_columns('event')
    print("\nActual database columns:")
    for col in columns:
        print(f"  - {col['name']}: {col['type']}")

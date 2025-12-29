import sqlite3
import os

db_path = os.path.join('instance', 'invitations.db')

if not os.path.exists(db_path):
    print(f"Database not found at {db_path}, checking root...")
    db_path = 'invitations.db'

print(f"Patching database at: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Add venue_latitude
    try:
        cursor.execute("ALTER TABLE event ADD COLUMN venue_latitude FLOAT")
        print("Added venue_latitude column.")
    except sqlite3.OperationalError as e:
        print(f"venue_latitude might already exist or error: {e}")

    # Add venue_longitude
    try:
        cursor.execute("ALTER TABLE event ADD COLUMN venue_longitude FLOAT")
        print("Added venue_longitude column.")
    except sqlite3.OperationalError as e:
        print(f"venue_longitude might already exist or error: {e}")

    conn.commit()
    conn.close()
    print("Database patched successfully.")

except Exception as e:
    print(f"Critical error patching DB: {e}")

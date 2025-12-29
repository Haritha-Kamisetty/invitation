import sqlite3
import os

# Correct DB based on config.py
db_path = 'instance/invitations.db'

print(f"Connecting to {db_path}")
if not os.path.exists(db_path):
    print("DB does not exist!")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("SELECT id, title, length(background_style), background_style FROM event ORDER BY created_at DESC LIMIT 1")
    row = cursor.fetchone()
    if row:
        print(f"Latest Event ID: {row[0]}")
        print(f"Title: {row[1]}")
        print(f"Background Style Length: {row[2]}")
        content = row[3]
        if content:
            print(f"Background Style Content (first 100): {content[:100]}")
            print(f"Background Style Content (last 100): {content[-100:]}")
        else:
            print("Background Style Content is NULL or Empty")
    else:
        print("No events found.")
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()

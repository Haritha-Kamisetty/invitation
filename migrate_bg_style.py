import sqlite3
import os

def migrate_db():
    db_path = 'instance/invitations.db'
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(event)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'background_style' not in columns:
            print("Adding background_style column to event table...")
            cursor.execute("ALTER TABLE event ADD COLUMN background_style VARCHAR(200)")
            conn.commit()
            print("Migration successful.")
        else:
            print("Column background_style already exists.")
            
    except Exception as e:
        print(f"Migration error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_db()

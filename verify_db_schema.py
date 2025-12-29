import sqlite3

def check_db_columns():
    print("Checking database columns...")
    # Point to the correct database file found in instance directory
    conn = sqlite3.connect('instance/invitations.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(event)")
    columns = [row[1] for row in cursor.fetchall()]
    conn.close()
    
    if 'contact_email' in columns and 'contact_phone' in columns:
        print("[SUCCESS] contact_email and contact_phone columns exist in 'event' table.")
    else:
        print("[ERROR] Missing columns in 'event' table.")
        print(f"Current columns: {columns}")

if __name__ == "__main__":
    check_db_columns()

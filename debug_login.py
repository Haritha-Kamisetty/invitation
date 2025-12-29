from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    # Check if any users exist
    users = User.query.all()
    print(f"Total users in database: {len(users)}")
    
    for user in users:
        print(f"\nUser: {user.email}")
        print(f"Name: {user.name}")
        print(f"Password hash exists: {bool(user.password_hash)}")
        print(f"Password hash length: {len(user.password_hash) if user.password_hash else 0}")
        
        # Test password verification
        test_password = "test123"  # Replace with actual password you're using
        result = user.check_password(test_password)
        print(f"Password 'test123' check result: {result}")

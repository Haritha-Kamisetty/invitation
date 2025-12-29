from app import create_app, db
from app.models import User

def reset_password(email, new_password):
    app = create_app()
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if user:
            print(f"User found: {user.name} ({user.email})")
            user.set_password(new_password)
            db.session.commit()
            print(f"SUCCESS: Password for {email} has been reset to: {new_password}")
            print("Please try creating a new session (restart browser) and logging in with this new password.")
        else:
            print(f"ERROR: No user found with email {email}")

if __name__ == "__main__":
    email = input("Enter the email address to reset: ").strip()
    password = input("Enter the new password: ").strip()
    if email and password:
        reset_password(email, password)
    else:
        print("Email and password are required.")

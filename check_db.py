from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
	try:
		db.create_all()
		print("Database created successfully")
		# Verify User table exists
		if User.query.first() is None:
			print("User table accessible")
	except Exception as e:
		print(f"Error: {e}")

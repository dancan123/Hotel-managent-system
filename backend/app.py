print("Starting backend app...")
import os
from flask import Flask
from flask_cors import CORS
from config import Config
from db import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
CORS(app)

# Register routes
from routes import api
app.register_blueprint(api)

# Database initialization
try:
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")
except Exception as e:
    print(f"Error creating database tables: {e}")

if __name__ == '__main__':
    print("Starting Flask app on http://127.0.0.1:5000")
    app.run(debug=False, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
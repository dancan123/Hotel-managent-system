from app import app, db
print('Import successful')
with app.app_context():
    db.create_all()
    print('DB created')
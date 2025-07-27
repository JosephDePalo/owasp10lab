from app import app, db, User

admin = User("admin")
admin.set_password("password123")


with app.app_context():
    db.drop_all()
    db.create_all()

    db.session.add(admin)
    db.session.commit()


print("Created database with user 'admin'")

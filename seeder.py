#!/usr/bin/env python3
from app import create_app
from app.models.base import db
from app.models.user import User, Role

app = create_app()  # Create app instance

def seed_data():
    with app.app_context():
        # Initialize database session
        with db.session.begin_nested():

            # Check if Role "admin" already exists
            admin_role = Role.query.filter_by(name="ADMIN").first()
            
            # If Role "ADMIN" does not exist, create it
            if not admin_role:
                admin_role = Role(name="ADMIN")
                db.session.add(admin_role)

            # Check if admin user already exists
            admin_user = User.query.filter_by(username="ADMIN").first()

            # If admin user does not exist, create it
            if not admin_user:
                admin_user = User(username="ADMIN", email="dev@dev.dev", password="dev")
                admin_user.roles.append(admin_role)
                db.session.add(admin_user)

        # Commit changes to the database
        db.session.commit()

if __name__ == "__main__":
    seed_data()

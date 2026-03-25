import auth_utils, models
from database import SessionLocal, engine

# Ensure tables exist
models.Base.metadata.create_all(bind=engine)

def create_admin():
    db = SessionLocal()
    try:
        # Check if admin already exists
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        if admin:
            print("Admin user already exists. Updating password...")
            admin.hashed_password = auth_utils.get_password_hash("admin123")
            admin.role = "admin"
            admin.free_generations_left = 9999
        else:
            print("Creating admin user...")
            hashed_password = auth_utils.get_password_hash("admin123")
            admin = models.User(
                username="admin",
                email="admin@voqube.com",
                hashed_password=hashed_password,
                role="admin",
                free_generations_left=9999
            )
            db.add(admin)
        
        db.commit()
        print("Admin user creation/update successful!")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()

import auth_utils, models
from database import SessionLocal, engine

# Ensure tables exist
models.Base.metadata.create_all(bind=engine)

def create_admin(target_username="navi@admin", target_password="navi_777"):
    db = SessionLocal()
    try:
        # Check if admin already exists
        admin = db.query(models.User).filter(models.User.username == target_username).first()
        if admin:
            print(f"Admin user '{target_username}' already exists. Updating password...")
            admin.hashed_password = auth_utils.get_password_hash(target_password)
            admin.role = "admin"
            admin.free_generations_left = 9999
        else:
            print(f"Creating admin user '{target_username}'...")
            hashed_password = auth_utils.get_password_hash(target_password)
            admin = models.User(
                username=target_username,
                email=f"{target_username.replace('@', '_')}@voqube.com",
                hashed_password=hashed_password,
                role="admin",
                free_generations_left=9999
            )
            db.add(admin)
        
        db.commit()
        print(f"Admin user '{target_username}' setup successful!")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()

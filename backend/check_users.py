import models
from database import SessionLocal

def check_users():
    db = SessionLocal()
    try:
        users = db.query(models.User).all()
        print(f"Total Users: {len(users)}")
        for u in users:
            print(f"ID: {u.id}, Username: {u.username}, Role: {u.role}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_users()

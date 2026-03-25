from sqlalchemy import create_engine, text
from database import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
with engine.begin() as conn:
    try:
        conn.execute(text("ALTER TABLE voice_generations ADD COLUMN is_deleted BOOLEAN DEFAULT 0"))
        print("Column added successfully or already exists.")
    except Exception as e:
        print("Error:", e)

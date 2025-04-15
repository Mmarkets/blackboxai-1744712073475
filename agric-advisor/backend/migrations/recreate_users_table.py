import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.user import User

DATABASE_URL = "sqlite:///./agric_advisor.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def recreate_users_table():
    db = SessionLocal()
    try:
        # Backup existing data
        users = db.execute(text("SELECT * FROM users")).fetchall()
        
        # Drop and recreate table with role column
        db.execute(text("DROP TABLE users"))
        db.execute(text("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                username VARCHAR,
                email VARCHAR,
                full_name VARCHAR,
                hashed_password VARCHAR,
                role VARCHAR(50) NOT NULL DEFAULT 'farmer'
            )
        """))
        
        # Restore data with default role
        for user in users:
            db.execute(
                text("""
                    INSERT INTO users 
                    (id, username, email, full_name, hashed_password, role) 
                    VALUES (:id, :username, :email, :full_name, :hashed_password, 'farmer')
                """),
                user
            )
        
        db.commit()
        print("Successfully recreated users table with role column")
    except Exception as e:
        db.rollback()
        print(f"Error recreating users table: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    recreate_users_table()

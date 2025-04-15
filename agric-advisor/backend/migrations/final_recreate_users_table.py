import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add the backend directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Database configuration
DATABASE_URL = "sqlite:///./agric_advisor.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def recreate_users_table():
    db = SessionLocal()
    try:
        # Backup existing data
        users = db.execute(text("SELECT * FROM users")).fetchall()
        
        # Drop and recreate table with role column
        db.execute(text("DROP TABLE IF EXISTS users"))
        db.execute(text("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                username VARCHAR NOT NULL,
                email VARCHAR NOT NULL,
                full_name VARCHAR,
                hashed_password VARCHAR NOT NULL,
                role VARCHAR(50) NOT NULL DEFAULT 'farmer',
                UNIQUE(username),
                UNIQUE(email)
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
                {
                    "id": user[0],  # id
                    "username": user[1],  # username
                    "email": user[2],  # email
                    "full_name": user[3],  # full_name
                    "hashed_password": user[4]  # hashed_password
                }
            )
        
        db.commit()
        print("Successfully recreated users table with role column")
    except Exception as e:
        db.rollback()
        print(f"Error recreating users table: {e}")
        print(f"Error details: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    recreate_users_table()

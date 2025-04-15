import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the backend directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Database configuration
DATABASE_URL = "sqlite:///./agric_advisor.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_role_column():
    db = SessionLocal()
    try:
        # Add the role column with direct SQL execution
        with engine.connect() as connection:
            connection.execute(
                'ALTER TABLE users ADD COLUMN role VARCHAR(50) NOT NULL DEFAULT "farmer"'
            )
        print("Successfully added 'role' column to users table")
    except Exception as e:
        print(f"Error adding role column: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_role_column()

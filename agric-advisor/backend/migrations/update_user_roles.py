import sys
import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

# Add the backend directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user import User

# Database configuration
DATABASE_URL = "sqlite:///./agric_advisor.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def update_user_roles():
    db = SessionLocal()
    try:
        # Check if 'role' column exists
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('users')]
        
        if 'role' not in columns:
            print("'role' column doesn't exist in users table")
            return
            
        users = db.query(User).all()
        updated_count = 0
        
        for user in users:
            if not hasattr(user, 'role') or user.role is None:
                user.role = "farmer"
                db.add(user)
                updated_count += 1
                
        db.commit()
        print(f"Updated roles for {updated_count} users")
    except Exception as e:
        db.rollback()
        print(f"Error updating user roles: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    update_user_roles()

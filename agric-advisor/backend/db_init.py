from config.database import engine, Base
from models.user import User
from models.crop import Crop
from models.disease import Disease

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()

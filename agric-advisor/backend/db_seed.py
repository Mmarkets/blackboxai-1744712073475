from config.database import SessionLocal
from models.user import User
from models.crop import Crop
from models.disease import Disease
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_data():
    db = SessionLocal()
    
    try:
        # Create sample users
        users = [
            User(
                username="farmer_john",
                email="john@example.com",
                full_name="John Farmer",
                hashed_password=pwd_context.hash("securepassword123")
            ),
            User(
                username="agri_expert",
                email="expert@example.com",
                full_name="Agricultural Expert",
                hashed_password=pwd_context.hash("expertpass456")
            )
        ]
        db.add_all(users)
        
        # Create sample crops
        crops = [
            Crop(
                name="Maize",
                description="A staple cereal crop grown worldwide",
                ideal_climate="Tropical and subtropical",
                planting_season="Early spring",
                growth_duration="3-4 months",
                water_requirements="Moderate"
            ),
            Crop(
                name="Tomato",
                description="Popular fruit vegetable with many varieties",
                ideal_climate="Warm temperate",
                planting_season="Spring",
                growth_duration="2-3 months",
                water_requirements="Regular"
            )
        ]
        db.add_all(crops)
        
        db.commit()  # Commit crops first to get IDs
        
        # Create sample diseases
        diseases = [
            Disease(
                name="Maize Rust",
                description="Fungal disease affecting maize leaves",
                symptoms="Orange-brown pustules on leaves",
                prevention="Use resistant varieties, crop rotation",
                treatment="Fungicide application",
                affected_crop_id=crops[0].id
            ),
            Disease(
                name="Tomato Blight",
                description="Common fungal disease in tomatoes",
                symptoms="Brown spots on leaves and fruit",
                prevention="Proper spacing, avoid overhead watering",
                treatment="Remove affected plants, apply fungicide",
                affected_crop_id=crops[1].id
            )
        ]
        db.add_all(diseases)
        
        db.commit()
        print("Sample data seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()

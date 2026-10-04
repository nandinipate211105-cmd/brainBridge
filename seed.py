import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import datetime

# Database Connection
MONGO_URL = "mongodb://127.0.0.1:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client["studentverse"]

# FIXED HASHING FOR PYTHON 3.14
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

async def seed():
    print("🌱 Cleaning old data...")
    await db.users.delete_many({})
    
    # Create a test user
    hashed_password = pwd_context.hash("password123")
    
    user = {
        "name": "Aryan Sharma",
        "email": "aryan@iitb.ac.in",
        "password": hashed_password,
        "user_id": "aryan_1234",
        "college": "IIT Bombay",
        "field": "BTech",
        "skills": ["Python", "AI", "React"],
        "created_at": datetime.datetime.utcnow()
    }
    
    await db.users.insert_one(user)
    print("✅ Successfully created user: aryan@iitb.ac.in")
    print("🔑 Password is: password123")

if __name__ == "__main__":
    asyncio.run(seed())
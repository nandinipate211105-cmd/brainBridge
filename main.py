import random
import string
import datetime
import bcrypt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Body, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient

# Add this function below your imports
def verify_password(plain_password: str, hashed_password: str):
    # This compares the typed password with the one in the database
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

app = FastAPI()

# --- CONFIGURATION ---
# REPLACE THESE WITH YOUR REAL DETAILS
GMAIL_ADDRESS = "nandinipate211105@gmail.com" 
GMAIL_APP_PASSWORD = "rbvxyinbhufjratr" # The 16-character code from Step 1

# Database Connection
MONGO_URL = "mongodb+srv://nandinipate211105_db_user:<db_password>@cluster0.rpuo3xu.mongodb.net/?appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URL)
db = client["studentverse"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- EMAIL SENDER FUNCTION ---
# In main.py
def send_otp_email(receiver_email, otp):
    print(f"DEBUG: Attempting to send email to {receiver_email}...")
    try:
        msg = MIMEMultipart()
        msg['From'] = f"StudentVerse <{GMAIL_ADDRESS}>"
        msg['To'] = receiver_email
        msg['Subject'] = f"{otp} is your StudentVerse Verification Code"

        # Simple HTML body
        body = f"""
        <html>
            <body style="font-family: sans-serif; padding: 20px;">
                <h2 style="color: #6366f1;">StudentVerse Ecosystem</h2>
                <p>Use the code below to verify your email and join the network:</p>
                <h1 style="background: #f1f5f9; padding: 10px; display: inline-block; letter-spacing: 5px;">{otp}</h1>
                <p>This code will expire soon.</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        # Use the exact same logic that worked in your debug script
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ SUCCESS: OTP {otp} sent to {receiver_email}")
        
    except Exception as e:
        print(f"❌ EMAIL ERROR: {e}")
        """
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #0f172a; color: white; padding: 20px;">
                <h2 style="color: #6366f1;">BrainBridge / StudentVerse</h2>
                <p>Welcome to the Ecosystem. Use the code below to verify your identity:</p>
                <div style="background: #1e1b4b; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #6366f1;">
                    <span style="font-size: 32px; font-weight: bold; color: #6366f1; letter-spacing: 5px;">{otp}</span>
                </div>
                <p style="font-size: 12px; color: #94a3b8; margin-top: 20px;">If you did not request this, please ignore this email.</p>
            </body>
        </html>
        """

        # Connect to Gmail SMTP
# --- ENDPOINTS ---

@app.post("/send-otp")
async def send_otp(background_tasks: BackgroundTasks, data: dict = Body(...)):
    email = data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
        
    otp = str(random.randint(100000, 999999))
    
    # Store OTP in DB
    await db.otp_verification.update_one(
        {"email": email},
        {"$set": {"otp": otp, "created_at": datetime.datetime.utcnow()}},
        upsert=True
    )
    
    # Send email in the background so the UI doesn't freeze
    background_tasks.add_task(send_otp_email, email, otp)
    
    return {"message": "OTP sent to your Gmail"}

@app.post("/verify-otp")
async def verify_otp(data: dict = Body(...)):
    email = data.get("email")
    otp = data.get("otp")
    record = await db.otp_verification.find_one({"email": email, "otp": otp})
    if not record:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    return {"message": "Verified"}

# --- REGISTRATION HELPER ---
def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

@app.post("/register")
async def register(user: dict = Body(...)):
    try:
        # Check if email exists
        existing = await db.users.find_one({"email": user['email']})
        if existing:
            raise HTTPException(status_code=400, detail="User already registered")

        # Create AI ID
        user_id = user['name'].split()[0].lower() + "_" + "".join(random.choices(string.digits, k=4))
        
        user['user_id'] = user_id
        user['password'] = hash_password(user['password'])
        user['created_at'] = datetime.datetime.utcnow()
        
        await db.users.insert_one(user)
        return {"user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# --- ADD THIS TO main.py ---

@app.post("/login")
async def login(data: dict = Body(...)):
    email = data.get("email")
    password = data.get("password")

    user = await db.users.find_one({"email": email})
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # This line was failing before, now it will work!
    if not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    return {
        "message": "Login Successful", 
        "user_id": user["user_id"], 
        "name": user["name"],
        "field": user.get("field", "Student")
    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)










# from fastapi import FastAPI, Depends, HTTPException
# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError, jwt # pip install python-jose
# from typing import List

# # 1. SECURITY CONFIG
# SECRET_KEY = "your_ultra_secret_key"
# ALGORITHM = "HS256"
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# # 2. AI MATCHING LOGIC (The "Ecosystem Brain")
# def calculate_match_score(user_skills: list, required_skills: list):
#     set1 = set(s.lower() for s in user_skills)
#     set2 = set(s.lower() for s in required_skills)
    
#     if not set2: return 0
    
#     # Jaccard Similarity Algorithm
#     intersection = set1.intersection(set2)
#     union = set1.union(set2)
#     return round((len(intersection) / len(union)) * 100, 1)

# @app.get("/api/ai/recommend-teams")
# async def get_team_recommendations(current_user_id: str):
#     user = await db.users.find_one({"user_id": current_user_id})
#     if not user: raise HTTPException(404, "User not found")
    
#     all_teams = await db.teams.find().to_list(100)
#     recommendations = []
    
#     for team in all_teams:
#         score = calculate_match_score(user["skills"], team["required_skills"])
#         if score > 10: # Only show relevant matches
#             team["match_percentage"] = score
#             recommendations.append(team)
            
#     return sorted(recommendations, key=lambda x: x["match_percentage"], reverse=True)
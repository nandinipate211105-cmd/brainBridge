import random
import datetime
import smtplib
from email.mime.text import MIMEText
from fastapi import FastAPI, HTTPException, Body, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from jose import jwt

# --- CONFIG ---
SECRET_KEY = "BRAINBRIDGE_ULTRA_SECRET"
ALGORITHM = "HS256"
# Replace with your Gmail and App Password
# Instructions: Google Account -> Security -> 2-Step Verification -> App Passwords
EMAIL_SENDER = "your-email@gmail.com"
EMAIL_PASSWORD = "your-app-password" 

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

db_client = AsyncIOMotorClient("mongodb://localhost:27017")
db = db_client.studentverse
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
# --- UTILS ---
def send_email(receiver, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = receiver
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

# --- FORGOT PASSWORD FLOW ---
@app.post("/api/auth/forgot-password")
async def forgot_password(email: str = Body(embed=True)):
    user = await db.users.find_one({"email": email})
    if not user: raise HTTPException(404, "Email not found")
    
    otp = str(random.randint(100000, 999999))
    # Store OTP in DB with 10-min expiry
    await db.otps.update_one({"email": email}, {"$set": {"otp": otp, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}}, upsert=True)
    
    send_email(email, "Reset Your BrainBridge Password", f"Your OTP is: {otp}")
    return {"message": "OTP sent to email"}

@app.post("/api/auth/reset-password")
async def reset_password(data: dict = Body(...)):
    record = await db.otps.find_one({"email": data["email"], "otp": data["otp"]})
    if not record or record["exp"] < datetime.datetime.utcnow():
        raise HTTPException(400, "Invalid or expired OTP")
    
    hashed_pwd = pwd_context.hash(data["new_password"])
    await db.users.update_one({"email": data["email"]}, {"$set": {"password": hashed_pwd}})
    await db.otps.delete_one({"email": data["email"]})
    return {"message": "Password updated successfully"}

# --- REAL-TIME CHAT ---
class ConnectionManager:
    def __init__(self): self.active_connections = {}
    async def connect(self, ws: WebSocket, user_id: str):
        await ws.accept()
        self.active_connections[user_id] = ws
    def disconnect(self, user_id: str): del self.active_connections[user_id]
    async def send_personal_message(self, message: dict, user_id: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/chat/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_json() # {target_id: "", msg: ""}
            await manager.send_personal_message({
                "from": user_id, 
                "message": data["msg"],
                "time": datetime.datetime.now().strftime("%H:%M")
            }, data["target_id"])
    except WebSocketDisconnect:
        manager.disconnect(user_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
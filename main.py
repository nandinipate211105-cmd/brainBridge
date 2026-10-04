# import os, random, datetime, smtplib, string
# from email.mime.text import MIMEText
# from fastapi import FastAPI, HTTPException, Body, BackgroundTasks
# from fastapi.middleware.cors import CORSMiddleware
# from motor.motor_asyncio import AsyncIOMotorClient
# from passlib.context import CryptContext

# app = FastAPI()
# app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# # --- DB CONNECTION (Bypassing SSL Issues) ---
# MONGO_URL = os.environ.get("MONGO_URL", "mongodb://127.0.0.1:27017")
# client = AsyncIOMotorClient(MONGO_URL, tlsAllowInvalidCertificates=True)
# db = client["studentverse"]

# # --- FIXED HASHING FOR PYTHON 3.14 ---
# pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# # --- SMTP GMAIL CONFIG ---
# GMAIL_ADDRESS = "nandinipate211105@gmail.com"
# GMAIL_APP_PASSWORD = "rbvxyinbhufjratr" 

# def send_otp_email(receiver_email, otp):
#     try:
#         msg = MIMEText(f"Welcome to the Verse. Your ID Verification Code is: {otp}")
#         msg['Subject'] = "Verification Code"
#         msg['From'] = f"StudentVerse <{GMAIL_ADDRESS}>"
#         msg['To'] = receiver_email

#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
#         server.send_message(msg)
#         server.quit()
#         print(f"✅ OTP Sent successfully to {receiver_email}")
#     except Exception as e:
#         print(f"❌ SMTP Error: {e}")
#         # In a real app, you would log this to the DB to notify the UI

# # --- ENDPOINTS ---

# @app.post("/send-otp")
# async def send_otp(bg_tasks: BackgroundTasks, data: dict = Body(...)):
#     email = data.get("email")
#     if not email: raise HTTPException(400, "Email required")
    
#     otp = str(random.randint(100000, 999999))
#     # Update or insert OTP
#     await db.otp_verification.update_one({"email": email}, {"$set": {"otp": otp}}, upsert=True)
    
#     # Send email without blocking the response
#     bg_tasks.add_task(send_otp_email, email, otp)
    
#     # IF OTP fails to reach, user can check the Terminal console to proceed (Debug)
#     return {"message": "OTP processing", "debug_info": "Check python terminal if email is delayed"}

# @app.post("/verify-otp")
# async def verify_otp(data: dict = Body(...)):
#     record = await db.otp_verification.find_one({"email": data["email"], "otp": data["otp"]})
#     if not record: raise HTTPException(400, "Invalid Code")
#     return {"message": "Verified"}

# @app.post("/register")
# async def register(user: dict = Body(...)):
#     # Check duplicate
#     existing = await db.users.find_one({"email": user['email']})
#     if existing: raise HTTPException(400, "Email already in system")

#     # Generate User ID
#     user['user_id'] = user['name'].split()[0].lower() + "_" + str(random.randint(1000, 9999))
#     user['password'] = pwd_context.hash(user['password']) # Use PBKDF2
    
#     res = await db.users.insert_one(user)
#     print(f"👤 User saved with ID: {user['user_id']}")
#     return {"user_id": user['user_id']}

# @app.post("/login")
# async def login(data: dict = Body(...)):
#     user = await db.users.find_one({"email": data["email"]})
#     if not user:
#         raise HTTPException(404, "Email not registered")
    
#     if not pwd_context.verify(data["password"], user["password"]):
#         raise HTTPException(401, "Wrong Access Key")
    
#     return {"name": user["name"], "user_id": user["user_id"], "field": user.get("field", "BTech")}


# @app.post("/api/ai/chat")
# async def ai_chat(data: dict = Body(...)):
#     user_msg = data.get("message", "").lower()
    
#     # 1. BRAINBRIDGE SPECIFIC LOGIC (Simulating "Google/ChatGPT" knowledge)
#     if "hello" in user_msg or "hi" in user_msg:
#         return {"answer": "Hi Nandini! I'm your StudentVerse AI. I can help you find hackathons, form teams, or navigate your profile. What's on your mind?"}
    
#     if "hackathon" in user_msg or "event" in user_msg:
#         return {"answer": "Based on current trends, there are 12 live events. Most students are currently looking at 'CodeCraft 25' and 'Math-X'. You can register for them in the Event Management tab."}
        
#     if "team" in user_msg or "squad" in user_msg:
#         return {"answer": "You can browse open squads in the 'Team Formation' section. Since you are in BTech, I recommend looking for teams needing Python or AI skills for a better match score!"}
    
#     if "who are you" in user_msg:
#         return {"answer": "I am the BrainBridge AI, an LLM-based assistant integrated into your ecosystem to make student collaboration seamless."}

#     # 2. FALLBACK SMART RESPONSE (Simulating General AI Knowledge)
#     return {"answer": f"That's an interesting question about '{user_msg}'. While I specialize in our student ecosystem, you might find more technical details on that by connecting with a mentor in the 'Discover' tab. Would you like me to help you find one?"}
# # AI logic goes here...
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)







































'''
import os, random, datetime, smtplib, string, httpx
from email.mime.text import MIMEText
from fastapi import FastAPI, HTTPException, Body, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from bson import ObjectId

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AsyncIOMotorClient("mongodb://127.0.0.1:27017", tlsAllowInvalidCertificates=True)
db = client["studentverse"]
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

GMAIL_ADDRESS = "nandinipate211105@gmail.com"
GMAIL_APP_PASSWORD = "rbvxyinbhufjratr" 


@app.post("/register")
async def register(user: dict = Body(...)):
    if await db.users.find_one({"email": user['email']}):
        raise HTTPException(400, "Email already registered")
    user['user_id'] = user['name'].split()[0].lower() + "_" + str(random.randint(1000, 9999))
    user['password'] = pwd_context.hash(user['password'])
    await db.users.insert_one(user)
    return {"user_id": user['user_id']}

@app.post("/login")
async def login(data: dict = Body(...)):
    user = await db.users.find_one({"email": data["email"]})
    if not user or not pwd_context.verify(data["password"], user["password"]):
        raise HTTPException(401, "Wrong Email or Password")
    return {"name": user["name"], "user_id": user["user_id"], "field": user.get("field", "BTech")}

@app.post("/api/auth/forgot-password")
async def forgot_password(email: str = Body(embed=True)):
    otp = str(random.randint(100000, 999999))
    await db.otps.update_one({"email": email}, {"$set": {"otp": otp, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}}, upsert=True)
    
    msg = MIMEText(f"Your StudentVerse Security Code is: {otp}")
    msg['Subject'] = "Reset Access"
    msg['From'] = GMAIL_ADDRESS
    msg['To'] = email
    
    with smtplib.SMTP('smtp.gmail.com', 587) as s:
        s.starttls()
        s.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        s.send_message(msg)
    return {"message": "Code sent"}


@app.post("/api/ai/chat")
async def ai_chat(data: dict = Body(...)):
    user_msg = data.get("message", "").lower()
    if "event" in user_msg:
        return {"answer": "You can find Live Events like CodeCraft in the Event Management tab!"}
    if "team" in user_msg:
        return {"answer": "Check the Team Formation section for open squads. Look for teams needing Python or AI skills!"}
    if "who are you" in user_msg:
        return {"answer": "I am the BrainBridge AI, an LLM-based assistant integrated into your ecosystem to make student collaboration seamless."}
    if "hello" in user_msg or "hi" in user_msg:
        return {"answer": "Hi! I'm your StudentVerse AI. I can help you find hackathons, form teams, or navigate your profile. What's on your mind?"}
    if "hackathon" in user_msg:
        return {"answer": "There are 12 live events. Most students are currently looking at 'CodeCraft 25' and 'Math-X'. You can register for them in the Event Management tab."}
    if "mentor" in user_msg:
        return {"answer": "You can find mentors in the Discover tab. I recommend looking for mentors with experience in your field of interest!"}
    if "profile" in user_msg:
        return {"answer": "You can update your profile in the Profile tab. Make sure to add your skills and field of study for better team matches!"}
    if "skills" in user_msg:
        return {"answer": "You can add your skills in the Profile tab. This will help you find teams and mentors that match your expertise!"}
    if "college" in user_msg:
        return {"answer": "You can update your college information in the Profile tab. This helps in connecting with peers from your institution!"}
    if "field" in user_msg:
        return {"answer": "You can update your field of study in the Profile tab. This will help you find relevant teams and mentors!"} 
    if "password" in user_msg:
        return {"answer": "If you forgot your password, you can reset it using the Forgot Password option on the login page. A security code will be sent to your email."}
    if "email" in user_msg:
        return {"answer": "You can update your email in the Profile tab. Make sure to verify your new email address for account security!"}
    if "Good morning" in user_msg or "Good evening" in user_msg:
        return {"answer": "Good day! How can I assist you in the StudentVerse today?"}
    if "Good night" in user_msg:
        return {"answer": "Good night! Don't forget to check your notifications before you sleep!"}
    if "thank you" in user_msg or "thanks" in user_msg:
        return {"answer": "You're welcome! I'm here to help you navigate the StudentVerse."}
    if "bye" in user_msg or "goodbye" in user_msg:
        return {"answer": "Goodbye! Feel free to reach out anytime you need assistance in the StudentVerse."}
    if "help" in user_msg:
        return {"answer": "Sure! You can ask me about events, teams, mentors, or how to navigate your profile. What do you need help with?"}
    
    responses = [
        f"Interesting question about {user_msg}. In the StudentVerse, we suggest collaborating with specialists in that field.",
        "That's a great thought! Have you checked the Discover tab for mentors on this topic?",
        "I can help with that. To get more info, maybe start a Team post in the Team Hub!"
    ]
    return {"answer": random.choice(responses)}


@app.post("/api/teams/create")
async def create_team(team: dict = Body(...)):
    team["created_at"] = datetime.datetime.utcnow()
    res = await db.teams.insert_one(team)
    return {"id": str(res.inserted_id)}

@app.get("/api/teams/list")
async def list_teams():
    teams = await db.teams.find().sort("created_at", -1).to_list(100)
    for t in teams: t["id"] = str(t["_id"]); del t["_id"]
    return teams

@app.post("/api/teams/apply")
async def apply_to_team(data: dict = Body(...)):
    notification = {
        "receiver_id": data["creator_id"], # Team maker's ID
        "sender_name": data["user_name"],
        "message": f"{data['user_name']} applied to your team!",
        "status": "unread",
        "timestamp": datetime.datetime.utcnow()
    }
    await db.notifications.insert_one(notification)
    return {"message": "Success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

'''





















'''
import os, random, datetime, smtplib, string, httpx
from email.mime.text import MIMEText
from fastapi import FastAPI, HTTPException, Body, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from bson import ObjectId

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

client = AsyncIOMotorClient("mongodb://127.0.0.1:27017", tlsAllowInvalidCertificates=True)
db = client["studentverse"]
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

@app.post("/register")
async def register(user: dict = Body(...)):
    user['user_id'] = user['name'].split()[0].lower() + "_" + str(random.randint(1000, 9999))
    user['password'] = pwd_context.hash(user['password'])
    await db.users.insert_one(user)
    return {"user_id": user['user_id']}

@app.post("/login")
async def login(data: dict = Body(...)):
    user = await db.users.find_one({"email": data["email"]})
    if not user or not pwd_context.verify(data["password"], user["password"]):
        raise HTTPException(401, "Invalid credentials")
    return {"name": user["name"], "user_id": user["user_id"]}

@app.post("/api/forge/create")
async def create_forge_entry(entry: dict = Body(...)):
    entry["created_at"] = datetime.datetime.utcnow()
    res = await db.forge_entries.insert_one(entry)
    
    notif = {
        "type": "global",
        "message": f"New {entry['type'].upper()} posted: {entry['title']}",
        "timestamp": datetime.datetime.utcnow(),
        "status": "unread"
    }
    await db.notifications.insert_one(notif)
    return {"id": str(res.inserted_id)}

@app.get("/api/forge/list")
async def get_forge_entries(category: str):
    # This ensures everyone sees the same list from DB
    cursor = db.forge_entries.find({"type": category}).sort("created_at", -1)
    entries = await cursor.to_list(length=100)
    for e in entries: e["id"] = str(e["_id"]); del e["_id"]
    return entries

# --- TEAMS ---
@app.post("/api/teams/create")
async def create_team(team: dict = Body(...)):
    team["created_at"] = datetime.datetime.utcnow()
    res = await db.teams.insert_one(team)
    # Global Notif
    await db.notifications.insert_one({
        "type": "global",
        "message": f"New Squad Formed: {team['name']} for {team['event']}",
        "timestamp": datetime.datetime.utcnow()
    })
    return {"id": str(res.inserted_id)}

@app.get("/api/teams/list")
async def list_teams():
    teams = await db.teams.find().sort("created_at", -1).to_list(100)
    for t in teams: t["id"] = str(t["_id"]); del t["_id"]
    return teams

@app.get("/api/notifications")
async def get_notifications():
    # Return last 20 global alerts
    notifs = await db.notifications.find().sort("timestamp", -1).limit(20).to_list(None)
    for n in notifs: n["id"] = str(n["_id"]); del n["_id"]
    return notifs

# --- ADD OR REPLACE THESE IN main.py ---

@app.get("/api/stats")
async def get_stats():
    # Calculate real numbers from DB
    u_count = await db.users.count_documents({})
    t_count = await db.teams.count_documents({})
    e_count = await db.forge_entries.count_documents({"type": "event"})
    
    # 12480 and 84 are your "base" dummy numbers from the UI
    return {
        "users": u_count + 12480, 
        "teams": t_count + 84, 
        "events": e_count + 12
    }

@app.post("/api/teams/create")
async def create_team(team: dict = Body(...)):
    team["created_at"] = datetime.datetime.utcnow()
    res = await db.teams.insert_one(team)
    
    # Add a notification for EVERYONE to see
    await db.notifications.insert_one({
        "type": "global",
        "message": f"New Squad Formed: {team['name']}",
        "timestamp": datetime.datetime.utcnow()
    })
    return {"id": str(res.inserted_id)}

@app.get("/api/notifications")
async def get_notifications():
    # Fetch ALL global notifications
    cursor = db.notifications.find().sort("timestamp", -1).limit(10)
    notifs = await cursor.to_list(None)
    for n in notifs: n["id"] = str(n["_id"]); del n["_id"]
    return notifs
# --- 4. ENDPOINTS: REAL AI CHAT ---

@app.post("/api/ai/chat")
async def ai_chat(data: dict = Body(...)):
    user_msg = data.get("message", "").lower()
    # If message is platform specific, answer manually
    if "event" in user_msg:
        return {"answer": "You can find Live Events like CodeCraft in the Event Management tab!"}
    if "team" in user_msg:
        return {"answer": "Check the Team Formation section for open squads. Look for teams needing Python or AI skills!"}
    if "who are you" in user_msg:
        return {"answer": "I am the BrainBridge AI, an LLM-based assistant integrated into your ecosystem to make student collaboration seamless."}
    if "hello" in user_msg or "hi" in user_msg:
        return {"answer": "Hi! I'm your StudentVerse AI. I can help you find hackathons, form teams, or navigate your profile. What's on your mind?"}
    if "hackathon" in user_msg:
        return {"answer": "There are 12 live events. Most students are currently looking at 'CodeCraft 25' and 'Math-X'. You can register for them in the Event Management tab."}
    if "mentor" in user_msg:
        return {"answer": "You can find mentors in the Discover tab. I recommend looking for mentors with experience in your field of interest!"}
    if "profile" in user_msg:
        return {"answer": "You can update your profile in the Profile tab. Make sure to add your skills and field of study for better team matches!"}
    if "skills" in user_msg:
        return {"answer": "You can add your skills in the Profile tab. This will help you find teams and mentors that match your expertise!"}
    if "college" in user_msg:
        return {"answer": "You can update your college information in the Profile tab. This helps in connecting with peers from your institution!"}
    if "field" in user_msg:
        return {"answer": "You can update your field of study in the Profile tab. This will help you find relevant teams and mentors!"} 
    if "password" in user_msg:
        return {"answer": "If you forgot your password, you can reset it using the Forgot Password option on the login page. A security code will be sent to your email."}
    if "email" in user_msg:
        return {"answer": "You can update your email in the Profile tab. Make sure to verify your new email address for account security!"}
    if "Good morning" in user_msg or "Good evening" in user_msg:
        return {"answer": "Good day! How can I assist you in the StudentVerse today?"}
    if "Good night" in user_msg:
        return {"answer": "Good night! Don't forget to check your notifications before you sleep!"}
    if "thank you" in user_msg or "thanks" in user_msg:
        return {"answer": "You're welcome! I'm here to help you navigate the StudentVerse."}
    if "bye" in user_msg or "goodbye" in user_msg:
        return {"answer": "Goodbye! Feel free to reach out anytime you need assistance in the StudentVerse."}
    if "help" in user_msg:
        return {"answer": "Sure! You can ask me about events, teams, mentors, or how to navigate your profile. What do you need help with?"}
    
    responses = [
        f"Interesting question about {user_msg}. In the StudentVerse, we suggest collaborating with specialists in that field.",
        "That's a great thought! Have you checked the Discover tab for mentors on this topic?",
        "I can help with that. To get more info, maybe start a Team post in the Team Hub!"
    ]
    return {"answer": random.choice(responses)}


@app.post("/api/teams/create")
async def create_team(team: dict = Body(...)):
    team["created_at"] = datetime.datetime.utcnow()
    res = await db.teams.insert_one(team)
    return {"id": str(res.inserted_id)}

@app.get("/api/teams/list")
async def list_teams():
    teams = await db.teams.find().sort("created_at", -1).to_list(100)
    for t in teams: t["id"] = str(t["_id"]); del t["_id"]
    return teams

@app.post("/api/teams/apply")
async def apply_to_team(data: dict = Body(...)):
    notification = {
        "receiver_id": data["creator_id"], # Team maker's ID
        "sender_name": data["user_name"],
        "message": f"{data['user_name']} applied to your team!",
        "status": "unread",
        "timestamp": datetime.datetime.utcnow()
    }
    await db.notifications.insert_one(notification)
    return {"message": "Success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
'''



















































import os, random, datetime, smtplib, string, httpx
from email.mime.text import MIMEText
from fastapi import FastAPI, HTTPException, Body, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from bson import ObjectId

app = FastAPI()

# --- SYSTEM FIX: ALLOW ALL CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DB & SECURITY ---
# Using Localhost for development; Bypassing SSL cert issues on Windows
client = AsyncIOMotorClient("mongodb://127.0.0.1:27017", tlsAllowInvalidCertificates=True)
db = client["studentverse"]
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# GMAIL CONFIG FOR OTP
GMAIL_ADDRESS = "nandinipate211105@gmail.com"
GMAIL_APP_PASSWORD = "rbvxyinbhufjratr" 

# --- EMAIL HELPERS ---
def send_otp_email(receiver, otp):
    try:
        body = f"<h2>Ecosystem Identity</h2><p>Your verification code to join StudentVerse is: <b>{otp}</b></p>"
        msg = MIMEText(body, 'html')
        msg['Subject'] = f"{otp} is your verification code"
        msg['From'] = f"StudentVerse Hub <{GMAIL_ADDRESS}>"
        msg['To'] = receiver
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        print(f"✅ OTP Sent to {receiver}")
    except Exception as e:
        print(f"❌ Mailer Error: {e}")


# --- 1. AUTH & IDENTITY ENDPOINTS ---

@app.post("/send-otp")
async def send_otp(bg_tasks: BackgroundTasks, data: dict = Body(...)):
    email = data.get("email")
    if not email: raise HTTPException(400, "Email required")
    otp = str(random.randint(100000, 999999))
    await db.otps.update_one({"email": email}, {"$set": {"otp": otp, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}}, upsert=True)
    bg_tasks.add_task(send_otp_email, email, otp)
    return {"message": "Processing..."}

@app.post("/verify-otp")
async def verify_otp(data: dict = Body(...)):
    record = await db.otps.find_one({"email": data["email"], "otp": data["otp"]})
    if not record: raise HTTPException(400, "Invalid/Expired OTP")
    return {"status": "verified"}

@app.post("/register")
async def register(user: dict = Body(...)):
    if await db.users.find_one({"email": user['email']}):
        raise HTTPException(400, "Already in Verse")
    user['user_id'] = user['name'].split()[0].lower() + "_" + str(random.randint(1000, 9999))
    user['password'] = pwd_context.hash(user['password'])
    await db.users.insert_one(user)
    return {"user_id": user['user_id']}

@app.post("/login")
async def login(data: dict = Body(...)):
    user = await db.users.find_one({"email": data["email"]})
    if not user or not pwd_context.verify(data["password"], user["password"]):
        raise HTTPException(401, "Denial: Invalid Access Key")
    return {"name": user["name"], "user_id": user["user_id"], "field": user.get("field", "BTech")}

# --- 2. GLOBAL HUB (DASHBOARD & STATS) ---
# --- ADD OR REPLACE IN main.py ---

@app.get("/api/discover/students")
async def discover_students(exclude_id: str):
    # Fetch everyone except YOU
    cursor = db.users.find({"user_id": {"$ne": exclude_id}}).limit(15)
    students = await cursor.to_list(length=15)
    for s in students:
        s["_id"] = str(s["_id"])
        # Standardize empty values so UI doesn't look broken
        s["college"] = s.get("college", "Ecosystem Member")
        s["skills"] = s.get("skills", ["Generalist"])
        if "password" in s: del s["password"]
    return students

@app.post("/api/connections/request")
async def send_connect(data: dict = Body(...)):
    await db.notifications.insert_one({
        "receiver_id": data["receiver_id"],
        "sender_name": data["sender_name"],
        "message": f"⚡ {data['sender_name']} sent you a Connection Link!",
        "timestamp": datetime.datetime.utcnow()
    })
    return {"status": "Link Sent"}

@app.get("/api/stats")
async def get_stats():
    u = await db.users.count_documents({})
    t = await db.teams.count_documents({})
    e = await db.forge_entries.count_documents({"type": "event"})
    return {"users": 12480 + u, "teams": 84 + t, "events": 12 + e}

@app.get("/api/notifications")
async def get_global_alerts():
    cursor = db.notifications.find().sort("timestamp", -1).limit(10)
    res = await cursor.to_list(None)
    for r in res: r["_id"] = str(r["_id"])
    return res

@app.get("/api/colleges/active")
async def active_colleges():
    cursor = db.users.aggregate([{"$group": {"_id": "$college", "count": {"$sum": 1}}}])
    return [{"name": c["_id"], "students": c["count"]} for c in await cursor.to_list(100)]

# --- 3. FORGE & TEAMS (CREATION & DISCOVERY) ---

@app.post("/api/forge/create")
async def create_forge(entry: dict = Body(...)):
    entry["created_at"] = datetime.datetime.utcnow()
    await db.forge_entries.insert_one(entry)
    await db.notifications.insert_one({
        "message": f"Global Update: New {entry['type']} '{entry['title']}' launched!",
        "timestamp": datetime.datetime.utcnow()
    })
    return {"status": "Created"}

@app.get("/api/forge/list")
async def list_forge(category: str):
    cursor = db.forge_entries.find({"type": category}).sort("created_at", -1)
    res = await cursor.to_list(50)
    for r in res: r["id"] = str(r["_id"]); del r["_id"]
    return res

@app.post("/api/teams/create")
async def create_team(team: dict = Body(...)):
    team["created_at"] = datetime.datetime.utcnow()
    await db.teams.insert_one(team)
    await db.notifications.insert_one({
        "message": f"Ecosystem Team Formed: {team['name']}",
        "timestamp": datetime.datetime.utcnow()
    })
    return {"status": "Squad Registered"}

@app.get("/api/teams/list")
async def get_teams():
    cursor = db.teams.find().sort("created_at", -1)
    res = await cursor.to_list(50)
    for r in res: r["id"] = str(r["_id"]); del r["_id"]
    return res

@app.post("/api/teams/apply")
async def apply_to_team(data: dict = Body(...)):
    await db.notifications.insert_one({
        "receiver_id": data["creator_id"],
        "message": f"{data['user_name']} applied to {data['team_name']}",
        "timestamp": datetime.datetime.utcnow()
    })
    return {"status": "Application Uploaded"}

# --- 4. SMART LOGIC & PERSISTENCE ---

@app.post("/api/feedback")
async def save_fb(fb: dict = Body(...)):
    await db.feedback.insert_one(fb)
    return {"status": "ok"}





@app.post("/api/ai/chat")
async def ai_chat(data: dict = Body(...)):
    user_msg = data.get("message", "").lower()
    # If message is platform specific, answer manually
    if "event" in user_msg:
        return {"answer": "You can find Live Events like CodeCraft in the Event Management tab!"}
    if "team" in user_msg:
        return {"answer": "Check the Team Formation section for open squads. Look for teams needing Python or AI skills!"}
    if "who are you" in user_msg:
        return {"answer": "I am the BrainBridge AI, an LLM-based assistant integrated into your ecosystem to make student collaboration seamless."}
    if "hello" in user_msg or "hi" in user_msg:
        return {"answer": "Hi! I'm your StudentVerse AI. I can help you find hackathons, form teams, or navigate your profile. What's on your mind?"}
    if "hackathon" in user_msg:
        return {"answer": "There are 12 live events. Most students are currently looking at 'CodeCraft 25' and 'Math-X'. You can register for them in the Event Management tab."}
    if "mentor" in user_msg:
        return {"answer": "You can find mentors in the Discover tab. I recommend looking for mentors with experience in your field of interest!"}
    if "profile" in user_msg:
        return {"answer": "You can update your profile in the Profile tab. Make sure to add your skills and field of study for better team matches!"}
    if "skills" in user_msg:
        return {"answer": "You can add your skills in the Profile tab. This will help you find teams and mentors that match your expertise!"}
    if "college" in user_msg:
        return {"answer": "You can update your college information in the Profile tab. This helps in connecting with peers from your institution!"}
    if "field" in user_msg:
        return {"answer": "You can update your field of study in the Profile tab. This will help you find relevant teams and mentors!"} 
    if "password" in user_msg:
        return {"answer": "If you forgot your password, you can reset it using the Forgot Password option on the login page. A security code will be sent to your email."}
    if "email" in user_msg:
        return {"answer": "You can update your email in the Profile tab. Make sure to verify your new email address for account security!"}
    if "Good morning" in user_msg or "Good evening" in user_msg:
        return {"answer": "Good day! How can I assist you in the StudentVerse today?"}
    if "Good night" in user_msg:
        return {"answer": "Good night! Don't forget to check your notifications before you sleep!"}
    if "thank you" in user_msg or "thanks" in user_msg:
        return {"answer": "You're welcome! I'm here to help you navigate the StudentVerse."}
    if "bye" in user_msg or "goodbye" in user_msg:
        return {"answer": "Goodbye! Feel free to reach out anytime you need assistance in the StudentVerse."}
    if "help" in user_msg:
        return {"answer": "Sure! You can ask me about events, teams, mentors, or how to navigate your profile. What do you need help with?"}
    
    responses = [
        f"Interesting question about {user_msg}. In the StudentVerse, we suggest collaborating with specialists in that field.",
        "That's a great thought! Have you checked the Discover tab for mentors on this topic?",
        "I can help with that. To get more info, maybe start a Team post in the Team Hub!"
    ]
    return {"answer": random.choice(responses)}


@app.post("/api/teams/create")
async def create_team(team: dict = Body(...)):
    team["created_at"] = datetime.datetime.utcnow()
    res = await db.teams.insert_one(team)
    return {"id": str(res.inserted_id)}

@app.get("/api/teams/list")
async def list_teams():
    teams = await db.teams.find().sort("created_at", -1).to_list(100)
    for t in teams: t["id"] = str(t["_id"]); del t["_id"]
    return teams

@app.post("/api/teams/apply")
async def apply_to_team(data: dict = Body(...)):
    notification = {
        "receiver_id": data["creator_id"], # Team maker's ID
        "sender_name": data["user_name"],
        "message": f"{data['user_name']} applied to your team!",
        "status": "unread",
        "timestamp": datetime.datetime.utcnow()
    }
    await db.notifications.insert_one(notification)
    return {"message": "Success"}
# --- ADD THESE TO main.py ---

# Get Real Students for the Suggestion List
@app.get("/api/discover/students")
async def discover_students(exclude_id: str):
    # Fetch all users except the one currently logged in
    cursor = db.users.find({"user_id": {"$ne": exclude_id}}).limit(10)
    students = await cursor.to_list(length=10)
    for s in students: 
        s["_id"] = str(s["_id"])
        # Ensure passwords never leave the server
        if "password" in s: del s["password"] 
    return students

# Send Connection Request
@app.post("/api/connections/request")
async def connection_request(data: dict = Body(...)):
    # data: { sender_id, sender_name, receiver_id }
    await db.notifications.insert_one({
        "receiver_id": data["receiver_id"],
        "type": "connection_request",
        "message": f"⚡ {data['sender_name']} wants to link with your Ecosystem DNA",
        "sender_id": data["sender_id"],
        "timestamp": datetime.datetime.utcnow()
    })
    return {"status": "Request Transmitted"}

@app.get("/")
async def root():
    return {"status": "online", "message": "BrainBridge API is live and running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
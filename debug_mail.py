import smtplib

SENDER_EMAIL = "nandinipate211105@gmail.com" 
# Use the 16-digit code with NO SPACES
APP_PASSWORD = "rbvxyinbhufjratr" 

def send_test():
    print("Connecting via Port 587...")
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() 
        server.login(SENDER_EMAIL, APP_PASSWORD)
        
        # This sends a test email to yourself
        server.sendmail(SENDER_EMAIL, SENDER_EMAIL, "Subject: StudentVerse Fixed\n\nLogin Successful!")
        server.quit()
        print("\n✅ SUCCESS: Check your Gmail inbox now!")
    except Exception as e:
        print(f"\n❌ STILL FAILING: {e}")

send_test()
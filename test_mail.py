import smtplib

GMAIL_ADDRESS = "your-email@gmail.com" 
GMAIL_APP_PASSWORD = "your-16-digit-password-no-spaces"

def test_email():
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, GMAIL_ADDRESS, "Subject: Test\n\nHello from StudentVerse!")
        server.quit()
        print("SUCCESS: Your email settings are correct. The mail should be in your inbox.")
    except Exception as e:
        print(f"FAILED: {e}")

test_email()
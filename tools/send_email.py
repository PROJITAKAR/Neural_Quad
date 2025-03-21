import smtplib
from email.message import EmailMessage
from config.config import SENDER_EMAIL, SENDER_PASSWORD


def send_email(to_email, subject, body):
    """Sends an email to the student with admission updates."""
    sender_email = SENDER_EMAIL
    sender_password = SENDER_PASSWORD
    
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email
    msg.add_alternative(body, subtype="html")
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        print("✅ SMTP Connection Successful")
        server.quit()
        success_msg = f"✅ Email sent successfully to {to_email}: {subject}"
        print(success_msg)  # 👈 This should appear in the terminal
        return success_msg  # 👈 Return this so CrewAI logs it
    except smtplib.SMTPAuthenticationError as e:
        error_msg = f"❌ Authentication failed: {e}"
    except smtplib.SMTPConnectError as e:
        error_msg = f"❌ Connection error: {e}"
    except smtplib.SMTPException as e:
        error_msg = f"❌ SMTP error: {e}"
    except Exception as e:
        error_msg = f"❌ General error: {e}"
    
    print(error_msg)  # 👈 Print it to terminal
    return error_msg  # 👈 Return it to CrewAI

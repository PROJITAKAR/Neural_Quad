import smtplib
from email.mime.text import MIMEText
from config.config import SENDER_EMAIL, SENDER_PASSWORD


def send_email(to_email, subject, body):
    sender_email = SENDER_EMAIL
    sender_password = SENDER_PASSWORD
    
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email
    
    try:
        server = smtplib.SMTP("smtp.example.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
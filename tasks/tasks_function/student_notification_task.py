from tools.send_email import send_email

# Notify students
def student_notification_task(student, status, message):
    subject = f"Admission Status Update: {status}"
    send_email(student["Email"], subject, message)
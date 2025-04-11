import smtplib
from email.message import EmailMessage
from config.config import SENDER_EMAIL, SENDER_PASSWORD, TO_EMAIL
import os
from crewai.tools import tool
import time
from email_templates.shortlisting_template import shortlisting_template
from email_templates.Not_Shortlisted_template import Not_Shortlisted_template
from email_templates.Loan_Not_Approved_template import Loan_Not_Approved_template
from email_templates.Loan_Approved_template import Loan_Approved_template
from email_templates.Doc_Error_template import Doc_Error_template

pdf_file= "Fee Structure.pdf"


# Define the email sending tool
@tool("send bulk email")
def send_bulk_email(students: list, subject: str, status_filter: str) -> str:
    """Sends emails only to students with the specified status."""

    sender_email = SENDER_EMAIL
    sender_password = SENDER_PASSWORD
    to_email = TO_EMAIL

    print(f"Students List: {students}")  
    print(f"Subject: {subject}")  
    print(f"Status Filter: {status_filter}")  

    parsed_students = []

    if (status_filter == "ERROR"):
        for student in students:
            parts = student.split(",")  # Split each student entry
            if len(parts) < 4:
                print(f"❌ Skipping invalid entry: {student}")
                continue  # Skip if the format is incorrect
            student_dict = {
                "id": parts[0],
                "name": parts[1],
                "email": parts[2],
                "doc_status": parts[3],
            }
            parsed_students.append(student_dict)
        print(f"Parsed Students: {parsed_students}")  # Debugging line
        # Filter students by status
        filtered_students = [s for s in parsed_students if status_filter in s["doc_status"]]

    if (status_filter == "Shortlisted" or status_filter == "Not Shortlisted"):
        for student in students:
            parts = student.split(",")  # Split each student entry
            if len(parts) < 5:
                print(f"❌ Skipping invalid entry: {student}")
                continue  # Skip if the format is incorrect
            admission_status = parts[4].split("(")[0].strip()
            student_dict = {
                "id": parts[0],
                "name": parts[1],
                "email": parts[2],
                "doc_status": parts[3],
                "shortlisting_status": admission_status
            }
            parsed_students.append(student_dict)
        print(f"Parsed Students: {parsed_students}")  # Debugging line
        # Filter students by status
        filtered_students = [s for s in parsed_students if s["shortlisting_status"] == status_filter]
    
    if (status_filter == "Loan Approved" or status_filter == "Loan Not Approved"):
        for student in students:
            parts = student.split(",")  # Split each student entry
            if len(parts) < 6:
                print(f"❌ Skipping invalid entry: {student}")
                continue  # Skip if the format is incorrect
            # admission_status = parts[5].split("(")[0].strip()
            student_dict = {
                "id": parts[0],
                "name": parts[1],
                "email": parts[2],
                "doc_status": parts[3],
                "shortlisting_status": parts[4],
                "loan_status": parts[5].split("(")[0].strip()
            }
            parsed_students.append(student_dict)
        print(f"Parsed Students: {parsed_students}")  # Debugging line
        # Filter students by status
        filtered_students = [s for s in parsed_students if s["loan_status"] == status_filter]

    
    if not filtered_students:
        return f"No students found with status: {status_filter}"
    print(f"Filtered Students: {filtered_students}")  # Debugging line

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        for student in filtered_students:
            recipient_email = student["email"]
            student_name = student["name"]
            print(f"📧 Sending email to: {recipient_email}")

            


            # Generate email body based on status
            if status_filter == "Shortlisted":
                body = shortlisting_template(student_name)
            elif status_filter == "Not Shortlisted":
                body = Not_Shortlisted_template(student_name)
            elif status_filter == "Loan Approved":
                body = Loan_Approved_template(student_name)
            elif status_filter == "Loan Not Approved":
                body = Loan_Not_Approved_template(student_name)
            elif status_filter == "ERROR":
                doc_error=student["doc_status"].replace("ERROR:", "").strip().split(",")
                doc_error = "".join(f"<li>{error.strip()}</li>" for error in doc_error)
                body= Doc_Error_template(student_name,doc_error)
            else:
                body = "<p>Thank you for your application. We will update you soon.</p>"

            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = sender_email
            msg["To"] =  to_email # ✅ Fixed: Now sends to the actual student
            msg.add_alternative(body, subtype="html")
            if (status_filter == "Shortlisted" and os.path.exists(pdf_file)):
                with open(pdf_file, "rb") as file:
                    msg.add_attachment(file.read(), maintype="application", subtype="pdf", filename="Fee_Structure.pdf")

            server.send_message(msg)
            print(f"✅ Email sent successfully to {recipient_email}")

            time.sleep(2)  # Pause between emails to avoid spam detection

        server.quit()
        return "✅ Emails sent successfully to all filtered students."

    except smtplib.SMTPAuthenticationError as e:
        return f"❌ Authentication failed: {e}"
    except smtplib.SMTPConnectError as e:
        return f"❌ Connection error: {e}"
    except smtplib.SMTPException as e:
        return f"❌ SMTP error: {e}"
    except Exception as e:
        return f"❌ General error: {e}"

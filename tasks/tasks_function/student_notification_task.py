from tools.send_email import send_email
import google.generativeai as genai
from config.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

# Function to generate email content using Gemini
def generate_email_content(status, student_name):
    """Generates email content using Google Gemini LLM."""
    prompt = f"""
    You are a student counselor. Generate a professional email in HTML format notifying {student_name} about their admission status: {status}.  

    - Use proper HTML tags for formatting.
    - Use <h2> for greetings, <p> for body text, and <b> for emphasis.
    - Include a polite and formal tone.
    - Do NOT include a subject line.
    - Provide clear next steps if needed.
    - Don't use ejs templates.
    - Write only about the admission status.
    - Ensure the email is readable and well-structured.
    - **Do NOT wrap the content in any code blocks.**
    - **Do NOT wrap the content in Markdown code blocks (e.g., ```html).**
    - Add inline CSS for styling (e.g., font-family, padding, etc.).
    """
    response = genai.chat(messages=[{"role": "user", "content": prompt}])
    return response.text




# Notify students
# Student Notification Task
def student_notification_task(student, status ,email):
    """Handles student admission notifications using Gemini-generated responses."""
    email_content = generate_email_content(status, student)  # Get AI-generated email
    return email_content
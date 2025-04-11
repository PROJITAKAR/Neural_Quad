from dotenv import load_dotenv
import os

# Get project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Construct path to .env file
dotenv_path = os.path.join(BASE_DIR, ".env")

# Load environment variables
load_dotenv(dotenv_path=dotenv_path)



SENDER_EMAIL = os.getenv("EMAIL")
SENDER_PASSWORD = os.getenv("PASSWORD")
GEMINI_API_KEY= os.getenv("GEMINI_API_KEY")
TO_EMAIL = os.getenv("TO_EMAIL")

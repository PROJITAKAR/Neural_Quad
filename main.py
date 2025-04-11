import time
from crews.admission_crew import admission_crew
from config.config import GEMINI_API_KEY
import google.generativeai as genai


genai.configure(api_key=GEMINI_API_KEY)

# Introduce a delay before starting
print("Starting validation... Please wait.")
time.sleep(2)  # Delay before kicking off the process

# Run validation for all students at once
result = admission_crew.kickoff()
print(result)
from crewai import Agent
from crewai import LLM
from tools.send_bulk_email import send_bulk_email

# Define the Student Counselor Agent
student_counselor = Agent(
    name="Student Counselor",
    role="Handles student communication through email",
    goal="Read student details from the list given by previous agent(batch_validator_agent or shortlisting_agent) and ensure each student receive timely updates on admission, missing documents, Shortlisting Status or loan approvals through email based on their status.",
    backstory=(
        "An AI-driven assistant for Institute of Engineering & Management College(IEM), ensuring students receive timely admission updates, "
        "iterating over each student in the list given by previous agent(batch_validator_agent or shortlisting_agent) and send email to student regarding their admission status."
        "Do not create or send email for student if their status shows 'Ok' in the list given by previous agent(batch_validator_agent or shortlisting_agent)"
        "send email to student regarding their admission status."
        "document reminders, and loan approvals. "
    ),
    memory=False,
    verbose=True,
    llm = LLM(
        model="gemini/gemini-2.0-flash",
        temperature=0.7,
    ),
    tools=[send_bulk_email]
)

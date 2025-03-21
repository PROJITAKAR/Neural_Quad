from crewai import Agent
from crewai import LLM


# Initialize Student Counselor Agent with Gemini LLM
student_counselor = Agent(
    name="Student Counselor",
    role="Handles student communication through {email}",
    goal="Ensure {student} receive timely updates on admission, missing documents, or loan approvals through {email} based on their {status}.",
    backstory=(
        "An AI-driven assistant for ABC College, ensuring students receive timely admission updates, "
        "send email to {student} regarding their admission {status}."
        "document reminders, and loan approvals. For further assistance, please contact admissions@abccollege.com. "
        "Note: This is an automated, no-reply email."
    ),
    verbose=True,
    llm = LLM(
        model="gemini/gemini-2.0-flash",
        temperature=0.7,
    )
)

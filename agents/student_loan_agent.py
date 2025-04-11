from crewai import Agent
from crewai import LLM
from crewai_tools import FileReadTool

csv_file_path = "Data/student_records.csv"

csv_reader = FileReadTool(file_path=csv_file_path)

# Define the Loan Approval Agent
loan_agent = Agent(
    role="Student Loan Officer",
    goal="Approve student loans based on eligibility criteria.",
    memory=False,
    verbose=True,
    backstory=(
        "You are a responsible loan officer evaluating student loan applications. "
        "You approve loans only if the student's family income is below 500,000, "
        "their shortlisting status in the list of students given by shortlisting_agent is 'Shortlisted', "
    ),
    tools=[csv_reader],
    llm=LLM(
        model="gemini/gemini-1.5-flash",
        temperature=0.7,
    ),
)
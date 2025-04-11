from crewai import Agent
from crewai import LLM
from crewai_tools import FileReadTool

csv_file_path = "Data/student_records.csv"

csv_reader = FileReadTool(file_path=csv_file_path)

# Define the Shortlisting Agent 
shortlisting_agent = Agent(
    role="Student Shortlisting Officer",
    goal="Shortlist students based on eligibility.",
    memory=False,
    verbose=True,
    backstory="You filter students based on predefined criteria for admissions.",
    tools=[csv_reader],
    llm=LLM(
        model="gemini/gemini-1.5-flash",
        temperature=0.7,
    ),
)
from crewai import Agent

student_counselor = Agent(
    name="Student Counselor", 
    role="Handles student communication", 
    goal="Communicate application status and resolve student queries."
)

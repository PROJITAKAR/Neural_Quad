from crewai import Agent

student_loan_agent = Agent(
    name="Student Loan Agent", 
    role="Processes student loans", 
    goal="Approve or reject loan applications based on criteria and budget."
)

from crewai import Agent

admission_officer = Agent(
    name="Admission Officer", 
    role="Oversees the admission process", 
    goal="Monitor and manage all admission activities."
)
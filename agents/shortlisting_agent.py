from crewai import Agent

shortlisting_agent = Agent(
    name="Shortlisting Agent", 
    role="Shortlists candidates based on eligibility and capacity", 
    goal="Identify and select eligible candidates."
)

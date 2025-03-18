from crewai import Agent

document_checking_agent = Agent(
    name="Document Checking Agent", 
    role="Validates applications and documents", 
    goal="Ensure all required documents are submitted and valid."
)

from crewai import Crew
from agents.admin_chatbot_agent import admin_chatbot_agent
from tasks.query_task import query_task

chatbot_crew=Crew(
    name="Admission Chatbot Crew",    
    agents=[admin_chatbot_agent],   
    tasks=[query_task],
    verbose=True,
)
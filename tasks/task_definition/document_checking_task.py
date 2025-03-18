from crewai import Task
from agents.document_checking_agent import document_checking_agent
from tasks.tasks_function.validate_application_task import validate_application_task

document_checking_task = Task(
    description="Validate student records and documents, then send results to Student Counselor", 
    agent=document_checking_agent, 
    function=validate_application_task
)

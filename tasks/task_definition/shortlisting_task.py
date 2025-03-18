from crewai import Task
from agents.shortlisting_agent import shortlisting_agent
from tasks.tasks_function.shortlist_candidates_task import shortlist_candidates_task

shortlisting_task = Task(
    description="Shortlist eligible candidates based on admission criteria and send results to Student Counselor", 
    agent=shortlisting_agent, 
    function=shortlist_candidates_task
)

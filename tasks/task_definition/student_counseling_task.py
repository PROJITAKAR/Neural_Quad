from crewai import Task
from agents.student_counselor import student_counselor
from tasks.tasks_function.student_notification_task import student_notification_task

student_counseling_task = Task(
    description="Notify students about missing documents, shortlisting status, or loan decisions", 
    agent=student_counselor, 
    function=student_notification_task
)

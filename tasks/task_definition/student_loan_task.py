from crewai import Task
from agents.student_loan_agent import student_loan_agent
from tasks.tasks_function.process_loan_task import process_loan_task

student_loan_task = Task(
    description="Process loan applications for shortlisted candidates and send results to Student Counselor", 
    agent=student_loan_agent, 
    function=process_loan_task
)

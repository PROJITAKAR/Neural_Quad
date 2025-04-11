from crewai import Crew
from agents.admission_officer import admission_officer_agent
from agents.document_checking_agent import batch_validator_agent
from agents.shortlisting_agent import shortlisting_agent
from agents.student_counselor import student_counselor
from agents.student_loan_agent import loan_agent
from tasks.document_checking_task import validate_all_students_task
from tasks.shortlisting_task import shortlisting_task
from tasks.student_counseling_task import student_counseling_task_1, student_counseling_task_2, student_counseling_task_3
from tasks.student_loan_task import loan_task
from tasks.store_progress_task import store_progress_task

# Define the crew for the admission process
admission_crew = Crew(
    name="IEM Admission Processing Crew",
    agents=[batch_validator_agent,student_counselor, shortlisting_agent,loan_agent,admission_officer_agent],
    tasks=[validate_all_students_task,student_counseling_task_1, shortlisting_task,student_counseling_task_2,loan_task, student_counseling_task_3,store_progress_task],
    process="sequential",
    verbose=True
)
from crewai import Crew
from agents.admission_officer import admission_officer
from agents.document_checking_agent import document_checking_agent
from agents.shortlisting_agent import shortlisting_agent
from agents.student_counselor import student_counselor
from agents.student_loan_agent import student_loan_agent
from tasks.task_definition.document_checking_task import document_checking_task
from tasks.task_definition.shortlisting_task import shortlisting_task
from tasks.task_definition.student_counseling_task import student_counseling_task
from tasks.task_definition.student_loan_task import student_loan_task


# Crew Definition
admission_crew = Crew(agents=[admission_officer, document_checking_agent, shortlisting_agent, student_counselor, student_loan_agent],
                      tasks=[document_checking_task, shortlisting_task, student_counseling_task, student_loan_task])

# document_checking_crew = Crew(
#     agents=[document_checking_agent],
#     tasks=[document_checking_task]
# )
from crewai import Task
from agents.student_counselor import student_counselor
from tasks.document_checking_task import validate_all_students_task
from tasks.shortlisting_task import shortlisting_task
from tasks.student_loan_task import loan_task
from tools.send_bulk_email import send_bulk_email

# Define the student counseling tasks for sending emails based on different statuses
# Task 1: Send email to students with document errors
student_counseling_task_1 = Task(
    description=(
        "Note: Only one email for each student.\n"
        "**Step 1: Read All Student Details**\n"
        "- Retrieve student details list from 'batch_validator_agent'.\n"
        "- Feed the list of students to step 2.\n"
        "**Step 2: Send Email(Doc Error)**\n"
        "- Filter students where status_filter = 'ERROR'.\n"
        "- Use the `send_bulk_email` tool to send an email to each student with a doc error.\n"
    ),
    agent=student_counselor,
    expected_output="Confirmation of whether an email was sent to each student with a doc error.",
    parameters=["students", "subject", "status_filter"],
    context=[validate_all_students_task],  # Ensure shortlisting_task is properly defined
    tools=[send_bulk_email],  # Ensure send_bulk_email is correctly registered
)

# Task 2: Send email to shortlisted and not shortlisted students
student_counseling_task_2 = Task(
    description=(
        "Note: Only one email for each student.\n"
        "**Step 1: Read All Student Details**\n"
        "- Retrieve student details list from 'shortlisting_agent'.\n"
        "- Ensure all students (both 'OK' and 'ERROR' cases) are included.\n"
        "- Feed the list of students to step 2.\n"
        "**Step 2: Send Email(Shortlisted)**\n"
        "- Filter students where status_filter = 'Shortlisted'.\n"
        "- Use the `send_bulk_email` tool to send an email to each shortlisted student.\n"
        "**Step 3: Send Emails (Not Shortlisted)**\n"
        "- After completing Step 2, filter students where status_filter = 'Not Shortlisted'.\n"
        "- Use the `send_bulk_email` tool to send an email to each non-shortlisted student."
    ),
    agent=student_counselor,
    expected_output="Confirmation of whether an email was sent to each student under both categories.",
    parameters=["students", "subject", "status_filter"],
    context=[shortlisting_task],  # Ensure shortlisting_task is properly defined
    tools=[send_bulk_email],  # Ensure send_bulk_email is correctly registered
)

# Task 3: Send email to students with loan approval status
student_counseling_task_3 = Task(
    description=(
        "Note: Only one email for each student.\n"
        "**Step 1: Read All Student Details**\n"
        "- Retrieve student details list from 'loan_agent'.\n"
        "- Remove student with Loan Not Requested"
        "- Remove student with NA status.\n"
        "- Feed the list of students to step 2.\n"
        "**Step 2: Send Email(Loan Approved)**\n"
        "- Filter students where status_filter = 'Loan Approved'.\n"
        "- Use the `send_bulk_email` tool to send an email to each student with Loan Approved .\n"
        "**Step 3: Send Emails (Loan Not Approved)**\n"
        "- After completing Step 2, filter students where status_filter = 'Loan Not Approved'.\n"
        "- Use the `send_bulk_email` tool to send an email to each student with Loan Not Approved ."
    ),
    agent=student_counselor,
    expected_output="Confirmation of whether an email was sent to each student under both categories.",
    parameters=["students", "subject", "status_filter"],
    context=[loan_task],  
    tools=[send_bulk_email],  
)

from crewai import Task
from agents.admission_officer import admission_officer_agent
from tasks.student_counseling_task import student_counseling_task_1, student_counseling_task_2, student_counseling_task_3
from tasks.document_checking_task import validate_all_students_task
from tasks.shortlisting_task import shortlisting_task
from tasks.student_loan_task import loan_task
from tools.store_students_progress_to_chroma import store_students_progress_to_chroma

store_progress_task = Task(
    description=(
        "You are the Admission Officer. Your job is to analyze each student's admission journey "
        "based on validation, shortlisting, loan approval, and email updates. "
        "Create a structured summary for each student and call the tool "
        "`store_students_progress_to_chroma(student_ids, names, summaries)` to save them all together.\n\n"
        "**Summary Format:**\n"
        "`Student ID: <ID> | Name: <Full Name> | Status: <Validation>, <Shortlisting>, <Loan Status>, Email Sent: Yes (<Reason>)`\n\n"
        "**Examples of ✅ Valid Summaries:**\n"
        "- `Student ID: S021 | Name: John Doe | Status: OK, Shortlisted, Loan Approved, Email Sent: Yes (Shortlisted & Loan Approved)`\n"
        "- `Student ID: S021 | Name: John Doe | Status: OK, Shortlisted, Loan Not Approved(family income>600000), Email Sent: Yes (Loan Not Approved)`\n"
        "- `Student ID: S021 | Name: John Doe | Status: OK, Shortlisted, Loan Not Requested, Email Sent: Yes (Shortlisted)`\n"
        "- `Student ID: S021 | Name: John Doe | Status: OK, Not Shortlisted(12th marks<45%), NA, Email Sent: Yes (Not Shortlisted)`\n"
        "- `Student ID: S021 | Name: John Doe | Status: ERROR: Invalid Student Phone Number, Not Shortlisted, NA, Email Sent: Yes (Document Error: Invalid Phone)`\n\n"
        "**❌ Invalid Summaries:**\n"
        "- ❌ `Loan Not Approved (Income Too High)` → Reason should not be included inside loan status field.\n"
        "- ❌ `Not Shortlisted(Rank above 9500)` → Reason must not be in the shortlisting field.\n"
        "- ❌ `Loan Not Approved (Doc Error)` → Loan field must be a plain value; move the reason to Email Sent.\n"
        "- ❌ `Loan Not Requested` without email reason → Reason must be in 'Email Sent' if relevant.\n\n"
        "**Important Notes:**\n"
        "- Validation can be `OK` or `ERROR: <reason>`\n"
        "- Shortlisting must be either `Shortlisted` or `Not Shortlisted`\n"
        "- Loan must be: `Loan Approved`, `Loan Not Approved`, or `Loan Not Requested`\n"
        "- Use `NA` if loan step doesn't apply (e.g., not shortlisted or validation error)\n"
        "- Always include `Email Sent: Yes (<short reason>)` at the end\n\n"
        "**Final Step:**\n"
        "Once all summaries are prepared, call the tool `store_students_progress_to_chroma(student_ids, names, summaries)` ONCE "
        "with all the data. Do not return plain text summaries or extra explanation."
    ),
    agent=admission_officer_agent,
    context=[
        validate_all_students_task,
        shortlisting_task,
        loan_task,
        student_counseling_task_1,
        student_counseling_task_2,
        student_counseling_task_3
    ],
    expected_output="All student progress summaries stored in ChromaDB in a single tool call.",
    tools=[store_students_progress_to_chroma]  # ✅ Updated tool
)

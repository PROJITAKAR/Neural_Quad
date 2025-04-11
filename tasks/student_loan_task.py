from crewai import Task
from agents.student_loan_agent import loan_agent
from tasks.shortlisting_task import shortlisting_task
from crewai_tools import FileReadTool

csv_file_path = "Data/student_records.csv"
csv_reader = FileReadTool(file_path=csv_file_path)


# Define the Loan Approval Task
loan_task = Task(
    description=(
        "**Step 1: Read Validation and Shortlisting Results**\n"
        "- Load the list of students given by shortlisting_agent to check if student is 'Shortlisted'.\n"
        "- If 'Not Shortlisted' , do not proceed further and mark loan status as 'NA'\n"
        "- If 'Shortlisted' , proceed to Step 2.\n\n"
        "**Step 2: Read Student Records**\n"
        "- Load `student_records.csv` to check if the student has requested a loan.\n"
        "- If no loan is requested, do not process further and mark loan status as 'Loan Not Requested'.\n"
        "- If loan is requested, check family income.\n"
        "- Approve loan if:\n"
        "   - **Family Income < 500,000**\n\n"
        "**Output Format:**\n"
        "- ✅Valid Output: `S021, John Doe, johndoe@example.com, OK, Shortlisted, Loan Approved`\n"
        "- ✅Valid Output: `S021, John Doe, johndoe@example.com, OK, Shortlisted, Loan Not Approved`\n"
        "- ✅Valid Output: `S021, John Doe, johndoe@example.com, OK, Shortlisted, Loan Not Requested`\n"
        "- ✅Valid Output: `S021, John Doe, johndoe@example.com, OK, Not Shortlisted, NA`\n"
        "- ✅Valid Output: `S021, John Doe, johndoe@example.com, ERROR: Invalid Student Phone Number, Not Shortlisted, NA`\n"
        "- ❌ Invalid Output: `S021, John Doe, johndoe@example.com, OK, Shortlisted, Loan Not Approved (Income Too High)`\n"
        "- ❌ Invalid Output (Not Shortlisted): `S022, Jane Smith, janesmith@example.com, OK, Not Shortlisted(Rank above 9500), Loan Not Approved`\n"
        "- ❌ Invalid Output(Doc Error): `S023, Alice Brown, alicebrown@example.com, ERROR: Invalid Student Phone Number, Not Shortlisted, Loan Not Approved (Doc Error)`\n"
        "- ❌ Invalid Output (No Loan Requested): `S024, Bob White, bobwhite@example.com, OK, Shortlisted, Loan Not Requested`"
    ),
    agent=loan_agent,
    tools=[csv_reader],
    context=[shortlisting_task],
    expected_output="A list of students with their loan approval status and reason if not approved.",
    # output_file="test.csv"
)

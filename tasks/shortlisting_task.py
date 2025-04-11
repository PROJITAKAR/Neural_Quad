from crewai import Task
from agents.shortlisting_agent import shortlisting_agent
from crewai_tools import FileReadTool
from tasks.document_checking_task import validate_all_students_task

csv_file_path = "Data/student_records.csv"

csv_reader = FileReadTool(file_path=csv_file_path)

# Define the Shortlisting Task
shortlisting_task = Task(
    description=(
        "**Step 1: Receive Validation Results from `batch_validator_agent`**\n"
        "- Get the list of students validated by `batch_validator_agent`.\n"
        "- If `doc_status` is `ERROR`, mark student as `Not Shortlisted (Doc Error)`.\n"
        "- If `doc_status` is `OK`, proceed to Step 2.\n\n"
        "**Step 2: Read Student Records**\n"
        "- Load `student_records.csv` to get academic details.\n"
        "- Shortlist students based on the following criteria:\n"
        "   - **10th Marks > 45%**\n"
        "   - **12th Marks > 45%**\n"
        "   - **Rank < 9500**\n\n"
        "**Output Format:**\n"
        "- ✅ Valid Output: `S001, John Doe, johndoe@example.com, OK, Shortlisted`\n"
        "- ❌ Invalid Output (Rank above 9500): `S001, John Doe, johndoe@example.com, OK, Not Shortlisted (Rank above 9500)`\n"
        "- ❌ Invalid Output (Doc Error): `S001, Jane Smith, janesmith@example.com, ERROR: Missing ID Proof, Not Shortlisted (Doc Error)`\n"
    ),
    agent=shortlisting_agent,
    tools=[csv_reader],
    context=[validate_all_students_task],
    expected_output="A list of all students with their shortlisting status and reason if not shortlisted."
)

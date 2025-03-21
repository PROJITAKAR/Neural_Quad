from crewai import Task
from agents.student_counselor import student_counselor
from tasks.tasks_function.student_notification_task import student_notification_task

student_counseling_task = Task(
    description=(
        "Send a formal notification email to {student} at {email} regarding their admission status: {status}. "
        "The email should provide updates on missing documents, shortlisting status, admission confirmation, "
        "or loan decisions, ensuring clear and timely communication."
    ), 
    agent=student_counselor, 
    function=student_notification_task,
    expected_output=("The generated email content as a string in **HTML format**, ready to be sent as an email."
                     "No Markdown formatting (e.g., no ```html or ```)"
    )
)

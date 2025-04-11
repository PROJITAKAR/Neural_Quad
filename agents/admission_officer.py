from crewai import Agent
from crewai import LLM
from tools.store_students_progress_to_chroma import store_students_progress_to_chroma

admission_officer_agent = Agent(
    role="Admission Officer",
    goal="Track and summarize the entire admission journey of each student",
    backstory=(
        "You are the university's Admission Officer. "
        "Your job is to gather and consolidate admission data from all processes: "
        "validation, shortlisting, loan approvals, and counseling. "
        "You must generate structured summaries for each student and store them in ChromaDB "
        "using the tool `store_students_progress_to_chroma(student_ids, names, summaries)`."
    ),
    verbose=True,
    llm=LLM(
        model="gemini/gemini-2.0-flash",
        temperature=0.7,
    ),
    tools=[store_students_progress_to_chroma]  # ✅ Updated tool
)
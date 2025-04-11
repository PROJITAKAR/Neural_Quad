from crewai import Agent
from crewai import LLM
from tools.chatbot_tools import fetch_student_summaries, format_student_summaries

admin_chatbot_agent = Agent(
    name="Admission Chatbot",
    role="Admission Assistant for Admin",
    goal="Answer admin queries about student admission progress and summaries",
    backstory="Helps IEM administrators by providing student-specific and overall admission progress.",
    verbose=True,
    llm=LLM(model="gemini/gemini-2.0-flash", temperature=0.7),
    tools=[fetch_student_summaries, format_student_summaries],
)
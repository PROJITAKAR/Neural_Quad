from crewai import Agent
from crewai import LLM
from crewai_tools import FileReadTool
from tools.check_documents import BatchPDFLoaderTool


# Define the document folder and CSV file path
doc_folder = "Data/student_docs"
csv_file_path = "Data/student_records.csv"

file_read_tool = FileReadTool(file_path=csv_file_path)
batch_pdf_loader_tool = BatchPDFLoaderTool(doc_folder=doc_folder)

# Define the Batch Validator Agent
batch_validator_agent = Agent(
    role="Batch Student Validator",
    goal="Validate multiple student records and their documents together.",
    memory=False,
    verbose=True,
    backstory=(
        "You are an expert in student data validation. "
        "You process all student records and their documents in one go, "
        "ensuring correctness, completeness, and compliance with regulations."
    ),
    tools=[file_read_tool,batch_pdf_loader_tool],  # Both tools used
    llm=LLM(model="gemini/gemini-1.5-flash", temperature=0.7),
    
)
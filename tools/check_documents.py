import os
from langchain_community.document_loaders import PyPDFLoader
from crewai.tools import BaseTool
from langchain.document_loaders import PyPDFLoader
from pydantic import Field
import time

# Required documents list
REQUIRED_DOCS = ["10th_marksheet.pdf", "12th_marksheet.pdf", "id_proof.pdf", "rank_card.pdf"]
OPTIONAL_DOCS = ["salary_slip.pdf"]  
 

# Define a tool to load PDFs for all students and validate missing ones
class BatchPDFLoaderTool(BaseTool):
    name: str = "Batch PDF Loader"
    description: str = "Loads and extracts text from all student documents in the given directory and checks for missing documents."

    doc_folder: str = Field(..., description="Path to the student documents folder.")

    def _run(self):
        """Loads PDFs from all student document folders and checks for missing files."""
        extracted_texts = {}

        for student_id in os.listdir(self.doc_folder):
            student_doc_folder = os.path.join(self.doc_folder, student_id)
            if os.path.isdir(student_doc_folder):
                extracted_texts[student_id] = {}
                missing_docs = []

                for doc_name in REQUIRED_DOCS:
                    file_path = os.path.join(student_doc_folder, doc_name)
                    if os.path.exists(file_path):  # Check if the document exists
                        try:
                            loader = PyPDFLoader(file_path)
                            pages = loader.load()
                            extracted_texts[student_id][doc_name] = "\n".join(
                                [page.page_content for page in pages if page.page_content]
                            )
                        except Exception as e:
                            extracted_texts[student_id][doc_name] = f"Error loading file: {str(e)}"
                    else:
                        missing_docs.append(doc_name)
                for doc_name in OPTIONAL_DOCS:
                    file_path = os.path.join(student_doc_folder, doc_name)
                    if os.path.exists(file_path):
                        try:
                            loader = PyPDFLoader(file_path)
                            pages = loader.load()
                            extracted_texts[student_id][doc_name] = "\n".join(
                                [page.page_content for page in pages if page.page_content]
                            )
                        except Exception as e:
                            extracted_texts[student_id][doc_name] = f"Error loading optional file: {str(e)}"
                # If any document is missing, record it
                if missing_docs:
                    extracted_texts[student_id]["missing_docs"] = f"Missing: {', '.join(missing_docs)}"

                time.sleep(0.5)  # Delay after processing each student

        time.sleep(1)  # Extra delay after all documents are loaded
        return extracted_texts
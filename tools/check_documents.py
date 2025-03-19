import os
import re
from langchain.document_loaders import PyPDFLoader

def extract_text_from_pdf(file_path):
    """Extract text from a given PDF file using LangChain's PyPDFLoader."""
    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        text = "\n".join([page.page_content for page in pages if page.page_content])
        return text.strip() if text else None
    except Exception:
        return None

def extract_marks_from_text(text):
    """Extracts subject-wise marks and calculates percentage."""
    subject_marks = re.findall(r"(\w+):\s*(\d{1,3})/(\d{1,3})", text)  # Example: "Math: 85/100"
    total_obtained = sum(int(marks) for _, marks, _ in subject_marks)
    total_max = sum(int(max_marks) for _, _, max_marks in subject_marks)
    
    if total_max > 0:
        percentage = (total_obtained / total_max) * 100
        return percentage
    return None

def check_documents(student_id, doc_folder, student_info):
    """Checks if required student documents are present, readable, and valid."""
    student_doc_folder = os.path.join(doc_folder, str(student_id))
    required_docs = ["10th_marksheet.pdf", "12th_marksheet.pdf", "id_proof.pdf", "rank_card.pdf"]
    missing_docs = []

    student_name = student_info["Name"]
    dob = student_info["Date of Birth"]
    rank = str(student_info["Rank"])
    marks_10th = student_info["10th Marks (%)"]
    marks_12th = student_info["12th Marks (%)"]

    for doc in required_docs:
        file_path = os.path.join(student_doc_folder, doc)
        
        if not os.path.exists(file_path):
            missing_docs.append(f"{doc} (missing)")
            continue
        
        text = extract_text_from_pdf(file_path)
        if not text:
            missing_docs.append(f"{doc} (unreadable)")
            continue

        if doc == "id_proof.pdf":
            dob = str(student_info["Date of Birth"])  # Convert to string before checking
            if student_name not in text or dob not in text:
                missing_docs.append(f"{doc} (mismatch: Name/DOB)")


        if doc == "rank_card.pdf":
            if student_name not in text or dob not in text or rank not in text:
                missing_docs.append(f"{doc} (mismatch: Name/DOB/Rank)")

        if doc == "10th_marksheet.pdf":
            extracted_10th_percentage = extract_marks_from_text(text)
            if extracted_10th_percentage and abs(extracted_10th_percentage - marks_10th) > 2:
                missing_docs.append(f"{doc} (Marks mismatch: Expected {marks_10th}, Found {extracted_10th_percentage:.2f})")

        if doc == "12th_marksheet.pdf":
            extracted_12th_percentage = extract_marks_from_text(text)
            if extracted_12th_percentage and abs(extracted_12th_percentage - marks_12th) > 2:
                missing_docs.append(f"{doc} (Marks mismatch: Expected {marks_12th}, Found {extracted_12th_percentage:.2f})")

    return missing_docs if missing_docs else "OK"

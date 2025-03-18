import os
from langchain.document_loaders import PyPDFLoader

# Check if all required documents are present & readable
def check_documents(student_id, doc_folder):
    required_docs = ["10th_marksheet.pdf", "12th_marksheet.pdf", "id_proof.pdf", "rank_card.pdf"]
    missing_docs = []
    
    for doc in required_docs:
        file_path = os.path.join(doc_folder, student_id, doc)
        if not os.path.exists(file_path):
            missing_docs.append(doc)
        else:
            try:
                loader = PyPDFLoader(file_path)
                pages = loader.load()
                if not pages:
                    missing_docs.append(doc)
            except Exception:
                missing_docs.append(doc)
    
    return missing_docs if missing_docs else "OK"
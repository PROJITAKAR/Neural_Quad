from tools.validate_csv_fields import validate_csv_fields
from tools.check_documents import check_documents 

# Validate student applications
def validate_application_task(student, doc_folder):
    valid_csv, csv_message = validate_csv_fields(student)
    missing_docs = check_documents(student["Student ID"], doc_folder)
    
    if valid_csv and missing_docs == "OK":
        return "OK"
    else:
        issues = []
        if not valid_csv:
            issues.append(csv_message)
        if missing_docs != "OK":
            issues.append(f"Missing/Unreadable: {', '.join(missing_docs)}")
        return "Issues: " + " | ".join(issues)
from tools.check_documents import check_documents 

# Validate CSV fields (email, marks, etc.)
def validate_csv_fields(student):
    if "@" not in student["Email"] or not student["Email"].endswith(('.com', '.org')):
        return False, "Invalid email format"
    if not (40 <= student["10th Marks (%)"] <= 100) or not (40 <= student["12th Marks (%)"] <= 100):
        return False, "Marks out of valid range"
    return True, "OK"
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
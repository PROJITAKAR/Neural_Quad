from tools.check_documents import check_documents 

import re
from datetime import datetime

def validate_csv_fields(student):
    # Validate Student ID (non-empty alphanumeric)
    if not student["Student ID"] or not student["Student ID"].isalnum():
        return False, "Invalid Student ID"

    # Validate Name (only letters and spaces)
    if not re.match(r"^[A-Za-z\s]+$", student["Name"]):
        return False, "Invalid Name"

    # Validate Email
    if "@" not in student["Email"] or not student["Email"].endswith(('.com', '.org')):
        return False, "Invalid email format"

    # Validate Phone Numbers (Student & Parents)
    if not re.match(r"^\d{10}$", student["Student Phone"]):
        return False, "Invalid Student Phone"
    if not re.match(r"^\d{10}$", student["Parents Phone"]):
        return False, "Invalid Parents Phone"

    # Validate Marks (10th & 12th) in range 40-100
    if not (40 <= student["10th Marks (%)"] <= 100):
        return False, "10th Marks out of range"
    if not (40 <= student["12th Marks (%)"] <= 100):
        return False, "12th Marks out of range"

    # Validate Rank (positive integer)
    if not str(student["Rank"]).isdigit() or int(student["Rank"]) <= 0:
        return False, "Invalid Rank"

    # Validate Family Income (non-negative number)
    if not isinstance(student["Family Income"], (int, float)) or student["Family Income"] < 0:
        return False, "Invalid Family Income"

    # Validate Category (Predefined categories)
    valid_categories = {"General", "SC", "ST", "OBC"}
    if student["Category"] not in valid_categories:
        return False, "Invalid Category"

    # Validate Date of Birth (YYYY-MM-DD) and Age
    try:
        dob = datetime.strptime(student["Date of Birth"], "%Y-%m-%d")
        age = (datetime.today() - dob).days // 365
        if not (17 <= age <= 22):
            return False, "Invalid Age"
    except ValueError:
        return False, "Invalid Date of Birth format"

    # Validate Gender
    if student["Gender"] not in {"Male", "Female", "Other"}:
        return False, "Invalid Gender"

    # Validate Address (Non-empty)
    if not student["Address"].strip():
        return False, "Address is empty"

    # Validate Loan Requested (Yes/No)
    if student["Loan Requested"] not in {"Yes", "No"}:
        return False, "Invalid Loan Requested value"

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
from crew import admission_crew
from tasks.tasks_function.validate_application_task import validate_application_task
from tasks.tasks_function.shortlist_candidates_task import shortlist_candidates_task
from tasks.tasks_function.process_loan_task import process_loan_task
from tasks.tasks_function.student_notification_task import student_notification_task
import pandas as pd

# Load student data CSV
def load_student_data(csv_path):
    return pd.read_csv(csv_path)
# Running the process
def run_admission_process(csv_path, doc_folder):
    student_data = load_student_data(csv_path)
    results = []
    
    for _, student in student_data.iterrows():
        doc_status = validate_application_task(student, doc_folder)
        if doc_status == "OK":
            shortlist_status = shortlist_candidates_task(student)
            loan_status = process_loan_task(student) if shortlist_status == "Shortlisted" else "N/A"
            message = f"Congratulations! You have been {shortlist_status}. Loan Status: {loan_status}."
        else:
            shortlist_status, loan_status = "N/A", "N/A"
            message = f"Your application has issues: {doc_status}. Please correct and resubmit."
        
        student_notification_task(student, shortlist_status, message)
        
        results.append({
            "Student ID": student["Student ID"],
            "Document Status": doc_status,
            "Shortlist Status": shortlist_status,
            "Loan Status": loan_status
        })
    
    results_df = pd.DataFrame(results)
    results_df.to_csv("admission_results.csv", index=False)
    print("Admission process completed. Results saved to admission_results.csv")

# Test Run
if __name__ == "__main__":
    csv_path = "student_records.csv"
    doc_folder = "docs"
    run_admission_process(csv_path, doc_folder)
    
    
# def run_document_checking(csv_path, doc_folder):
#     student_data = load_student_data(csv_path)
#     results = []
    
#     for _, student in student_data.iterrows():
#         doc_status = validate_application_task(student["Student ID"], doc_folder, student)  # ✅ Pass student_id
#         results.append({
#             "Student ID": student["Student ID"],
#             "Document Status": doc_status
#         })
    
#     results_df = pd.DataFrame(results)
#     results_df.to_csv("document_check_results.csv", index=False)
#     print("Document checking process completed. Results saved to document_check_results.csv")

# if __name__ == "__main__":
#     csv_path = "student_records.csv"
#     doc_folder = "student_docs"
#     run_document_checking(csv_path, doc_folder)
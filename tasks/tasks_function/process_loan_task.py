
# Process loan applications
def process_loan_task(student):
    if student["Family Income"] < 500000:  # Example threshold for loan approval
        return "Loan Approved"
    return "Loan Rejected"
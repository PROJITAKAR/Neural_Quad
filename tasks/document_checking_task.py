from crewai import Task
from agents.document_checking_agent import batch_validator_agent
from crewai_tools import FileReadTool
from tools.check_documents import BatchPDFLoaderTool

# Define the document folder and CSV file path
doc_folder = "Data/student_docs"
csv_file_path = "Data/student_records.csv"

file_read_tool = FileReadTool(file_path=csv_file_path)
batch_pdf_loader_tool = BatchPDFLoaderTool(doc_folder=doc_folder)


# Define the validation task
validate_all_students_task = Task(
    description=(
        "**Step 1: Read All Student Records**\n"
        "- Load all student data from the CSV file.\n"
        "- Validate each student's details against the given rules.\n\n"
        "   - **Student ID**: Alphanumeric and non-empty.\n"
        "   - **Name**: Should only contain letters and spaces.\n"
            "   - **Email**: Must have '@' and end in .com or .org.\n"
            "   - **Phone Numbers**: Exactly 10 digits.\n"
            "   - **Marks**:\n"
            "       - 10th Marks: 40-100%.\n"
            "       - 12th Marks: 40-100%.\n"
            "   - **Rank**: Positive integer > 0.\n"
            "   - **Family Income**: Non-negative number.\n"
            "   - **Category**: One of 'GEN', 'SC', 'ST', 'OBC'.\n"
            "   - **Date of Birth**: Format 'DD-MM-YYYY', year between 2002-2005.\n"
            "   - **Gender**: 'M', 'F', or 'Other'.\n"
            "   - **Address**: Cannot be empty.\n"
            "   - **Loan Requested**: 'Yes' or 'No'.\n\n"
        "**Step 2: Validate All Student Documents**\n"
        "- Load all student PDFs using the Batch PDF Loader tool.\n"
        "- Ensure that each student has the required documents:\n"
        "   - 10th_marksheet.pdf\n"
        "   - 12th_marksheet.pdf\n"
        "   - id_proof.pdf\n"
        "   - rank_card.pdf\n"
        "   - if the student has Loan Requested then salary_slip.pdf should be present"
        "- Identify missing or unreadable documents.\n\n"
        "*Step 3: Match CSV Data With Extracted PDF Content*\n"
        "- For each student ID:\n"
        "   - Use the extracted content from the Batch PDF Loader tool.\n"
        "   - Match the following fields between the CSV and the corresponding PDF documents:\n\n"
        "   1. *Name*\n"
        "      - Must match exactly (case-sensitive, character-for-character) in:\n"
        "        - id_proof.pdf\n"
        "        - 10th_marksheet.pdf\n"
        "        - 12th_marksheet.pdf\n"
        "        - rank_card.pdf\n"
        "      - Mismatch format: ERROR: Name mismatch in [filename] (CSV: <csv_name>, PDF: <pdf_name>)\n\n"
        "   2. *Date of Birth*\n"
        "      - Must match exactly in all 4 documents above.\n"
        "      - Format must be DD-MM-YYYY.\n"
        "      - Mismatch format: ERROR: DOB mismatch in [filename] (CSV: <csv_dob>, PDF: <pdf_dob>)\n\n"
        "   3. *Category*\n"
        "      - Must match exactly in rank_card.pdf.\n"
        "      - Mismatch format: ERROR: Category mismatch (CSV: <csv_category>, PDF: <pdf_category>)\n\n"
        "   4. *Rank*\n"
        "      - Must match exactly in rank_card.pdf. No tolerance for +/- differences.\n"
        "      - Mismatch format: ERROR: Rank mismatch (CSV: <csv_rank>, PDF: <pdf_rank>)\n\n"
        "   5. *Gender*\n"
        "      - Must match exactly in id_proof.pdf.\n"
        "      - Accepted values: M, F, Other (must match CSV exactly).\n"
        "      - Mismatch format: ERROR: Gender mismatch (CSV: <csv_gender>, PDF: <pdf_gender>)\n\n"
        "   6. *Address*\n"
        "      - Must match exactly (including commas and spacing) in id_proof.pdf.\n"
        "      - Mismatch format: ERROR: Address mismatch (CSV: <csv_address>, PDF: <pdf_address>)\n\n"
        "   7. *10th Percentage*\n"
        "      - Extracted from 10th_marksheet.pdf.\n"
        "      - Compare against 10th_percentage in CSV.\n"
        "      - Acceptable difference: +0.50 or -0.50\n"
        "      - Example: CSV :84.00 and PDF: 83.80 → no ERROR\n"
        "      - Mismatch format: ERROR: 10th Percentage mismatch (CSV: <csv_pct>, PDF: <pdf_pct>)\n\n"
        "   8. *12th Percentage*\n"
        "      - Extracted from 12th_marksheet.pdf.\n"
        "      - Compare against 12th_percentage in CSV.\n"
        "      - Acceptable difference: ±0.50\n"
        "      - Example: CSV 84.00 and PDF 83.80 → OK; CSV 82.00 and PDF 81.1 → Mismatch\n"
        "      - Mismatch format: ERROR: 12th Percentage mismatch (CSV: <csv_pct>, PDF: <pdf_pct>)\n\n"
        "- If any mismatch is found, include them in the final result line for the student.\n"
        "- If all fields match exactly, include OK in the result.\n"
        "**Output Format:**\n"
        "- ✅ Valid Output: `S001, John Doe, johndoe@example.com, OK`\n"
        "- ✅ Valid Outputt: `S001, John Doe, johndoe@example.com, ERROR: Missing ID Proof, Invalid Phone Number`\n"
        "- ❌ Invalid Output: `S001, John Doe, johndoe@example.com, 9842430267, OK`\n"
        "- no phone number in output\n"
    ),
    agent=batch_validator_agent,
    tools=[file_read_tool,batch_pdf_loader_tool],
    expected_output="A structured list of student validation results, including CSV and document errors."
)
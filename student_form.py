import streamlit as st
import os
import csv
from datetime import datetime

# Get next Student ID
def get_next_student_id(csv_path="Data/student_records.csv"):
    if not os.path.exists(csv_path):
        return "S001"
    try:
        with open(csv_path, "r") as f:
            reader = csv.reader(f)
            rows = list(reader)
            if not rows:
                return "S001"
            last_id = rows[-1][0]
            num = int(last_id[1:]) + 1
            return f"S{num:03d}"
    except:
        return "S001"

student_id = get_next_student_id()

st.title("🎓 IEM Student Admission Form")

st.markdown("🔒 **Note:** All fields are mandatory unless marked optional. Ensure that the information you provide matches the documents you upload!")

with st.form("admission_form"):
    st.markdown(f"### Your Student ID: `{student_id}`")

    name = st.text_input("Full Name *")
    email = st.text_input("Email *")
    phone = st.text_input("Student Phone Number *")
    marks_10 = st.number_input("10th Marks (%) *", min_value=0.0, max_value=100.0, step=0.1)
    marks_12 = st.number_input("12th Marks (%) *", min_value=0.0, max_value=100.0, step=0.1)
    father_name = st.text_input("Father's Name *")
    mother_name = st.text_input("Mother's Name *")
    parents_phone = st.text_input("Parent's Contact Number *")
    rank = st.number_input("Entrance Exam Rank *", min_value=0)
    income = st.number_input("Family Income (INR) *", min_value=0)
    category = st.selectbox("Category *", ["GEN", "SC", "ST", "OBC"])
    dob = st.date_input("Date of Birth *", min_value=datetime(2002, 1, 1), max_value=datetime(2005, 12, 31))
    gender = st.selectbox("Gender *", ["M", "F", "Other"])
    address = st.text_area("Address *")
    loan_requested = st.selectbox("Do you want a loan? *", ["Yes", "No"])

    st.markdown("#### 📎 Upload Documents (PDFs only)")
    id_proof = st.file_uploader("ID Proof *", type=["pdf"])
    marksheet_10 = st.file_uploader("10th Marksheet *", type=["pdf"])
    marksheet_12 = st.file_uploader("12th Marksheet *", type=["pdf"])
    rank_card = st.file_uploader("Rank Card *", type=["pdf"])
    salary_slip = st.file_uploader("Salary Slip (Optional, only if applying for loan)", type=["pdf"])

    submitted = st.form_submit_button("Submit")

if submitted:
    missing_docs = not all([id_proof, marksheet_10, marksheet_12, rank_card])
    missing_fields = not all([name, email, phone, father_name, mother_name, parents_phone, address])

    if missing_docs or missing_fields:
        st.error("❌ Please fill all required fields and upload all required documents.")
    else:
        # Save CSV row
        with open("Data/student_records.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                student_id, name, email, phone, marks_10, marks_12,
                father_name, mother_name, parents_phone,
                rank, income, category, dob.strftime("%d-%m-%Y"),
                gender, address, loan_requested
            ])

        # Save docs
        student_dir = f"Data/student_docs/{student_id}"
        os.makedirs(student_dir, exist_ok=True)

        def save_pdf(file, filename):
            if file:
                with open(os.path.join(student_dir, filename), "wb") as f:
                    f.write(file.read())

        save_pdf(id_proof, "id_proof.pdf")
        save_pdf(marksheet_10, "10th_marksheet.pdf")
        save_pdf(marksheet_12, "12th_marksheet.pdf")
        save_pdf(rank_card, "rank_card.pdf")
        save_pdf(salary_slip, "salary_slip.pdf")

        st.success(f"✅ Submission successful! Your Student ID is `{student_id}`.")


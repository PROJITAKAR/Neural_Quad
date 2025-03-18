
# Validate CSV fields (email, marks, etc.)
def validate_csv_fields(student):
    if "@" not in student["Email"] or not student["Email"].endswith(('.com', '.org')):
        return False, "Invalid email format"
    if not (40 <= student["10th Marks (%)"] <= 100) or not (40 <= student["12th Marks (%)"] <= 100):
        return False, "Marks out of valid range"
    return True, "OK"
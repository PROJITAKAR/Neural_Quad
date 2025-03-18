

# Shortlist candidates based on eligibility
def shortlist_candidates_task(student):
    if student["10th Marks (%)"] >= 75 and student["12th Marks (%)"] >= 75 and student["Rank"] < 5000:
        return "Shortlisted"
    return "Not Shortlisted"
import pandas as pd

# Load student data CSV
def load_student_data(csv_path):
    return pd.read_csv(csv_path)
import pandas as pd
import os

def load_data(file_name):
    try:
        # Construct the file path
        file_path = os.path.join("..", "backend", "data", file_name)
        
        # Load the data
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"file not found: {e}")
        return None
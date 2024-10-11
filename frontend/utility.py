import pandas as pd
import os

def load_data(file_name):
    try:
        file_path = os.path.join(os.path.dirname(__file__), '../backend/data', file_name)
        data = pd.read_csv(file_path)
        return data
    except Exception as ex:
        raise ex
    
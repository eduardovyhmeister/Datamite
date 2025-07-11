"""A short script to replace JSON lists in a CSV file with comma-separated values.
To run this script, use the 'python manage.py runscript clean_csv_from_json' command while 
inside the project folder. This will replace existing CSVs so make sure you know what you
are doing!
"""

import csv
import json
import os.path


# Paths to the CSV files containing the data:
DATA_FOLDER = os.path.join("ANPAHP", "data")
BSC_FAMILIES_CSV_PATH = os.path.join(DATA_FOLDER, "BSC_families.csv")
BSC_SUBFAMILIES_CSV_PATH = os.path.join(DATA_FOLDER, "BSC_subfamilies.csv")
OBJECTIVES_CSV_PATH = os.path.join(DATA_FOLDER, "Objectives.csv")
CRITERIA_CSV_PATH = os.path.join(DATA_FOLDER, "Criteria.csv")
KPIS_CSV_PATH = os.path.join(DATA_FOLDER, "KPIs.csv")


def clean_csv(filepath: str, savepath:str = None):
    """Cleans the provided CSV file from JSON lists. If `savepath` is specified,
    then it is used for the new file, otherwise, the old file is overwritten.
    
    Args:
        filepath (str): The path to the CSV file to clean.
        savepath (str): The path for the new version of the file, if set to `None`,
            then the old file is overwritten.
    """
    if not savepath:
        savepath = filepath
        
    # Read the file:
    lines = []
    with open(filepath, "r") as csv_file:
        reader = csv.reader(csv_file, quotechar = '"', delimiter = ',',
                            quoting = csv.QUOTE_ALL, skipinitialspace = True,
                            escapechar = "\\")
        for row in reader:
            line = []
            for column in row:
                try:
                    o = json.loads()
                    if isinstance(o, list):
                        line.append(" ,".join(o)) # Replace the list with comma-separated values
                    else:
                        line.append(column)
                except json.decoder.JSONDecodeError: # Not a JSON object
                    line.append(column)
            line_str = ", ".join([f'"{column}"' for column in line])
            lines.append(line_str)
        
    # Rewrite the file:
    with open(savepath, "w") as f:
        for line in lines:
            f.write(f"{line}\n")
    
    
    
if __name__ == "__main__":
    clean_csv(KPIS_CSV_PATH, "test.csv")
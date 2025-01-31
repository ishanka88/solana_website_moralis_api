from website.methods import coinTransactions
from website import db
from flask import flash
import os
import json


def addFromPendingFolder(file_name):
    main_folder = 'bigquery_data/pending_database'
    if not os.path.exists(main_folder):
        message = "Error - There is no files available (bigquerry_dat folder not exist)"
        return False , message
                   
    file_path = os.path.join(main_folder,file_name)

    if not os.path.exists(file_path):
        message = f"Error - The coin file ('{file_path}')  does not exist at the bigquery_data folder'."
        return False, message
    
    try:
        # Open the JSON file in read mode
        with open(file_path, 'r') as file:
            # Load the content of the file into a Python dictionary
            file_all_data = json.load(file)
            data = file_all_data["data"]
            
            if data :
                result = coinTransactions.addCoinTransactions(file_all_data)
                return result
            else :
                message = "Error : Transaction Data not avialble in the file (file save error)"
                return False, message
        
    except FileNotFoundError:
        message = "error File not found"
        return False, message
    except json.JSONDecodeError:
        message ="error : Error decoding JSON"
        return False, message

    except Exception as e:
        return False, str(e)
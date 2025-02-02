from website.methods import coinTransactions
from website.modles import db,AvailableCoinSets, CoinTransactions ,Pairs,Gainers,BackupFolder,MoralisApiKey
from website import db
from flask import flash
import os
import json
import shutil


def addFromPendingFolder(file_name,rowId):
    pending_folder = 'coin_data_from_moralis/pending_database'
    if not os.path.exists(pending_folder):
        message = "Error - There is no files available (coin_data_from_moralis folder not exist)"
        return False , message
                   
    pending_folder_file_path = os.path.join(pending_folder,file_name)

    if not os.path.exists(pending_folder_file_path):
        message = f"Error - The coin file ('{pending_folder_file_path}')  does not exist at the coin_data_from_moralis/pending_database folder'."
        return False, message
    
    try:
        # Open the JSON file in read mode
        with open(pending_folder_file_path, 'r') as file:
            # Load the content of the file into a Python dictionary
            file_all_data = json.load(file)
            data = file_all_data["data"]
            
            if data :
                result = coinTransactions.addCoinTransactions(file_all_data)
                if result[0]:
                    set_number = result[2]
                    BackupFolder.update_set_number_by_id(rowId,set_number)
                    added_folder = 'coin_data_from_moralis/added_database'
                    added_folder_file_path = os.path.join(added_folder,file_name)
                    shutil.move(pending_folder_file_path, added_folder_file_path)

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
    

def deleteFromPendingFolder(file_name):
    try:
        pending_folder = 'coin_data_from_moralis/pending_database'
        if not os.path.exists(pending_folder):
            message = "Error - There is no files available (coin_data_from_moralis folder not exist)"
            return False , message
                    
        pending_folder_file_path = os.path.join(pending_folder,file_name)

        if not os.path.exists(pending_folder_file_path):
            message = f"Error - The coin file ('{pending_folder_file_path}')  does not exist at the coin_data_from_moralis/pending_database folder'."
            return False, message


        delete_folder = 'coin_data_from_moralis/delete_data'
        delete_folder_file_path = os.path.join(delete_folder,file_name)

        shutil.move(pending_folder_file_path, delete_folder_file_path)
        
        message= "Successfuly Deleted"
        return True, message
    
    except FileNotFoundError:
        message = "error File not found"
        return False, message
    except json.JSONDecodeError:
        message ="error : Error decoding JSON"
        return False, message

    except Exception as e:
        return False, str(e)
    
def deleteFromAddedFolder(file_name):
    try:
        added_folder = 'coin_data_from_moralis/added_database'
        if not os.path.exists(added_folder):
            message = "Error - There is no files available (coin_data_from_moralis folder not exist)"
            return False , message
                    
        added_folder_file_path = os.path.join(added_folder,file_name)

        if not os.path.exists(added_folder_file_path):
            message = f"Error - The coin file ('{added_folder_file_path}')  does not exist at the coin_data_from_moralis/pending_database folder'."
            return False, message


        delete_folder = 'coin_data_from_moralis/delete_data'
        delete_folder_file_path = os.path.join(delete_folder,file_name)

        shutil.move(added_folder_file_path, delete_folder_file_path)
        
        message= "Successfuly Deleted"
        return True, message
    
    except FileNotFoundError:
        message = "error File not found"
        return False, message
    except json.JSONDecodeError:
        message ="error : Error decoding JSON"
        return False, message

    except Exception as e:
        return False, str(e)
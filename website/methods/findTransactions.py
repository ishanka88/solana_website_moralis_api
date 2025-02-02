import os
import json
import threading
import requests
from flask import flash
from website.modles import MoralisApiKey,BackupFolder
import os
import json
import threading  # Added to run the cancel in the background
import time
from config import Config


# Store job_id and client in thread-local storage
thread_data = threading.local()

def fetch_data(api_key, contract_address, from_date, to_date, cursor=None):
    url = f"https://solana-gateway.moralis.io/token/mainnet/{contract_address}/swaps?fromDate={from_date}&toDate={to_date}&order=DESC"
    
    if cursor:
        url += f"&cursor={cursor}"  # Add cursor for pagination if provided
    
    headers = {
        "Accept": "application/json",
        "X-API-Key": api_key
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    

def save_data_into_json_file(status,final_data,ticker,contract_address,cursor,fromDateTime,toDateTime,
                          low_value,peak_value,description,priority):
    

    main_folder = 'coin_data_from_moralis'
    subfolders = ["pending_database", "added_database","partialy_ran", "backup_data","delete_data"]

    if not os.path.exists(main_folder):
        print("moralis_data main folder does not exist, creating it...")
        os.makedirs(main_folder)
        for folder in subfolders:
            folder_path = os.path.join(main_folder, folder)
            if not os.path.exists(folder_path):
                print(f"Creating folder: {folder_path}...")
                os.makedirs(folder_path)

    txns = len(final_data)
    from_signature = final_data[-1].get('transactionHash') 
    from_block_timestamp = final_data[-1].get('blockTimestamp')
    to_signature = final_data[0].get('transactionHash') 
    to_block_timestamp = final_data[0].get('blockTimestamp')
    set_number=0
    coin_data = {
        "ticker": ticker,
        "contract_address": contract_address,
        "set_number": set_number,
        "last_cursor":cursor,
        "searched_from_date_time": fromDateTime,
        "searched_to_date_time": toDateTime,
        "from_signature": from_signature,
        "to_signature": to_signature,
        "from_block_timestamp": from_block_timestamp,
        "to_block_timestamp": to_block_timestamp,
        "low_value": low_value,
        "peak_value": peak_value,
        "description": description,
        "txns":txns,
        "priority": priority,
        "data": final_data
    }

    file_name = f"{contract_address}_{from_block_timestamp}_to_{to_block_timestamp}.json"
    backup_data_file_path = os.path.join(main_folder, "backup_data", file_name)
    pending_database_file_path = os.path.join(main_folder, "pending_database", file_name)
    partialy_ran_database_file_path = os.path.join(main_folder, "partialy_ran", file_name)

    def write_to_json(file_path, data):
        try:
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            print(f"Data has been written to {file_path}")
        except Exception as e:
            print(f"Error writing to {file_path}: {e}")

    write_to_json(backup_data_file_path, coin_data)
    print("Data has been written to backup data Folder")
    flash("Data has been written to backup data Folder")


    if status:
        write_to_json(pending_database_file_path, coin_data)

        addDetails =BackupFolder.add_record(ticker,set_number,contract_address,fromDateTime,toDateTime,from_signature,to_signature,from_block_timestamp,to_block_timestamp,low_value,peak_value,description,priority,txns,file_name,1)
        if addDetails :
            message = "Successful - json file added to the pending folder"
            print(message)
            flash(message)
            return True, message
        else:
            message = "Error - json file added to the pending folder but not in to database backup table\n Error - This will not show in the ADD COIN SET"
            print(message)
            flash(message,'error')
            return False, message 
            
        
    else:
        write_to_json(partialy_ran_database_file_path, coin_data)
        addDetails =BackupFolder.add_record(ticker,set_number,contract_address,fromDateTime,toDateTime,from_signature,to_signature,from_block_timestamp,to_block_timestamp,low_value,peak_value,description,priority,txns,file_name,0)
        if addDetails :
            message = "Unsuccessful - json file added to the partially ran folder"
            print(message)
            flash(message)
            return False, message
        else:
            message = "Error - json file added to the partially ran folder but not in to database backup table\n Error - This will not show in the ADD COIN SET"
            print(message)
            flash(message, 'error')
            return False, message 




def get_transactions_from_Date_and_Time(contract_address, ticker, fromDateTime, toDateTime, low_value, peak_value, description, priority):
   
        try :
            Config.SHOULD_STOP = False

            contract_address=contract_address
            fromDateTime =fromDateTime
            toDateTime = toDateTime
            moralis_databse_last_row =  MoralisApiKey.get_last_item()
            if not moralis_databse_last_row :
                message =  "Please Set API (api is not available in database)"
                return False, message

            moralis_api_key = moralis_databse_last_row.api_key

            final_data = []
            total_data_fetched = 0
            cursor = None  # Initialize cursor as None for the first request


            while True:
                if Config.SHOULD_STOP :  # Check if the stop flag is set
                    print("Process stopped by user.")
                    flash("Process stopped by user.", 'error')
                    responce =save_data_into_json_file(False,final_data,ticker,contract_address,cursor,fromDateTime,toDateTime,
                          low_value,peak_value,description,priority)
                
                    print("Error: Partialy saved data")
                    flash("Partialy saved data",'error')
                    return responce

                data = fetch_data(moralis_api_key, contract_address, fromDateTime, toDateTime, cursor)

                if not data or 'result' not in data:
                    message = "No more data or error encountered."
                    print(message)
                    return False, message
                   

                result_length = len(data['result'])
                if result_length == 0:
                    message ="No data found in the response."
                    print(message)
                    return False, message

                final_data.extend(data['result'])  # Append only the result data
                total_data_fetched += result_length

                # Update the cursor to fetch next page of data if available
                cursor = data.get("cursor")

                # If no cursor is returned, it means there are no more pages of data
                if not cursor:
                    break

                print(f"Fetched {result_length} records, Total fetched: {total_data_fetched}.")

                # Optional: Sleep for a few seconds before the next request to prevent rate-limiting
                time.sleep(0.5)

            if final_data:
                txns = len(final_data)
                print(f"Found {txns} transactions for Coin: {contract_address}")
                flash(f"Found {txns} transactions for Coin: {contract_address}",'message')

                responce =save_data_into_json_file(True,final_data,ticker,contract_address,cursor,fromDateTime,toDateTime,
                          low_value,peak_value,description,priority)
                
                return responce

            else:
                print("No data to save.")
                flash("No data to save.",'error')

                message =f"Error :No data to save.\n Check entered data is correct"
                print(message)
                return False, message


        except Exception as e:
            if final_data:
                responce=save_data_into_json_file(False,final_data,ticker,contract_address,cursor,fromDateTime,toDateTime,
                          low_value,peak_value,description,priority)
                
                print("Error: Partialy saved data")
                flash("Partialy saved data",'error')
                print(f"Error ; {str(e)}")
                flash(f"Error ; {str(e)}",'error')

                return responce
            else:
                print("Error: No data to save.")
                flash("Error :No data to save.",'error')
                print(f"Error ; {str(e)}")
                flash(f"Error ; {str(e)}",'error')

                message =f"Error :No data to save.\n {str(e)}"
                print(message)
                return False, message

            




# import requests
# from flask import flash
# from website.modles import Credentials
# from google.cloud import bigquery
# from google.oauth2 import service_account
# from datetime import datetime
# from decimal import Decimal
# import os
# import json
# import threading  # Added to run the cancel in the background


# # Store the job_id and cancel_thread in a global scope or session
# thread_data = threading.local()

# def cancel_bigquery_job(client, job_id):
#     """Cancels the running BigQuery job."""
#     try:
#         job = client.get_job(job_id)  # Fetch the job instance
#         job.cancel()  # Cancel the job
#         print(f"Job {job_id} has been canceled.")
#     except Exception as e:
#         print(f"Error canceling job {job_id}: {str(e)}")

# def get_transactions_from_Date_and_Time(contract_address, ticker, fromDateTime, toDateTime, low_value, peak_value, discription, priority):
#     global job_id, cancel_thread

#     # Initialize BigQuery client
#     if not os.path.exists("credential_folder"):
#         print("credential_folder does not exist, creating it...")
#         os.makedirs("credential_folder")
#         message = "Error - No credential file found. Add it."
#         return False, message

#     credential_file = Credentials.get_last_item().credentil_file_name

#     if not credential_file:
#         message = "Error - No credential file found. Add it."
#         return False, message

#     key_path = os.path.join("credential_folder", credential_file)

#     # Set up credentials using the service account key
#     credentials = service_account.Credentials.from_service_account_file(key_path)

#     # Initialize BigQuery client with the credentials
#     client = bigquery.Client(credentials=credentials, project=credentials.project_id)

#     # Define the query for BigQuery
#     query = f"""
#     SELECT 
#         tt.signature, 
#         tt.block_timestamp,
#         tt.pre_token_balances,
#         tt.post_token_balances,
#         tt.accounts
#     FROM 
#         `bigquery-public-data.crypto_solana_mainnet_us.Transactions` AS tt
#     WHERE 
#         EXISTS (
#             SELECT 1
#             FROM UNNEST(tt.accounts) AS account
#             WHERE account.pubkey = '{contract_address}'  
#         )
#         AND tt.block_timestamp BETWEEN '{fromDateTime}' AND '{toDateTime}'
#         AND tt.status = 'Success'
#     ORDER BY 
#         tt.block_timestamp DESC;
#     """

#     try:
#         # Start the BigQuery query
#         query_job = client.query(query)  # Start the query
#         job_id = query_job.job_id  # Store the job_id for cancellation later

#         # Setup a background thread to handle cancellation
#         cancel_thread = threading.Thread(target=cancel_bigquery_job, args=(client, job_id))
#         cancel_thread.start()

#         # Wait for the query to complete or be cancelled
#         results = query_job.result()  # This will block until the job completes or is canceled

#         # Process results if query was successful
#         if results.total_rows > 0:
#             try:
#                 print(f"Found {results.total_rows} transactions for wallet: {contract_address}")

#                 from_signature = results[0].signature
#                 from_block_timestamp = results[0].block_timestamp
#                 to_signature = results[-1].signature
#                 to_block_timestamp = results[-1].block_timestamp

#                 coin_data = {
#                     "ticker": ticker,
#                     "contract_address": contract_address,
#                     "searched_from_date_time": fromDateTime,
#                     "searched_to_date_time": toDateTime,
#                     "from_signature": from_signature,
#                     "to_signature": to_signature,
#                     "from_block_timestamp": from_block_timestamp,
#                     "to_block_timestamp": to_block_timestamp,
#                     "low_value": low_value,
#                     "peak_value": peak_value,
#                     "discription": discription,
#                     "priority": priority,
#                     "data": results
#                 }

#                 main_folder = 'bigquery_data'
#                 subfolders = ["pending_database", "added_database", "backup_data"]

#                 if not os.path.exists(main_folder):
#                     print("bigquery_data main folder does not exist, creating it...")
#                     os.makedirs(main_folder)

#                 def create_folders(folders):
#                     for folder in folders:
#                         folder_path = os.path.join(main_folder, folder)
#                         if not os.path.exists(folder_path):
#                             print(f"Creating folder: {folder_path}...")
#                             os.makedirs(folder_path)

#                 create_folders(subfolders)

#                 file_name = f"{contract_address}_{from_block_timestamp}_to_{to_block_timestamp}.json"
#                 backup_data_file_path = os.path.join(main_folder, "backup_data", file_name)
#                 pending_database_file_path = os.path.join(main_folder, "pending_database", file_name)

#                 def write_to_json(file_path, data):
#                     try:
#                         with open(file_path, 'w') as json_file:
#                             json.dump(data, json_file, indent=4)
#                         print(f"Data has been written to {file_path}")
#                     except Exception as e:
#                         print(f"Error writing to {file_path}: {e}")

#                 write_to_json(backup_data_file_path, coin_data)
#                 write_to_json(pending_database_file_path, coin_data)

#                 print(f"Data has been written to {backup_data_file_path}")

#                 message = "Successful - json file added to the pending folder"
#                 return True, message

#             except Exception as e:
#                 print(e)
#                 message = "Error - json file did not add to any folder"
#                 return False, message
#         else:
#             message = "No data found (Zero data from BigQuery)."
#             return False, message

#     except Exception as e:
#         print(e)
#         message = "Unknown error happened while requesting BigQuery. Please check login credentials."
#         return False, message


# def cancel_bigquery_job(client, job_id):
#     """Cancels the running BigQuery job"""
#     try:
#         job = client.get_job(job_id)  # Fetch the job instance
#         job.cancel()  # Cancel the job
#         print(f"Job {job_id} has been canceled.")
#     except Exception as e:
#         print(f"Error canceling job {job_id}: {str(e)}")

# def get_transactions_from_Date_and_Time(contract_address, ticker, fromDateTime, toDateTime, low_value, peak_value, discription, priority):

#     # Your function to initiate BigQuery jobs
#     global job_id, cancel_thread
#     # After starting the job:
#     query_job = client.query(query)  # This starts the job
#     job_id = query_job.job_id  # Store the job id for cancellation later

#     # Monitor the job using threading for cancelation
#     cancel_thread = threading.Thread(target=cancel_bigquery_job, args=(client, job_id))
#     cancel_thread.start()

#     try:
#         contract_address = contract_address
#         ticker = ticker
#         fromDateTime = fromDateTime
#         toDateTime = toDateTime

#         ##################################
#         if not os.path.exists("credential_folder"):
#             print("credential_folder does not exist, creating it...")
#             os.makedirs("credential_folder")
#             message = "Error - No credential file found. Add it."
#             return False, message

#         credential_file = Credentials.get_last_item().credentil_file_name

#         if not credential_file:
#             message = "Error - No credential file found. Add it."
#             return False, message

#         key_path = os.path.join("credential_folder", credential_file)

#         # Set up credentials using the service account key
#         credentials = service_account.Credentials.from_service_account_file(key_path)

#         # Initialize BigQuery client with the credentials
#         client = bigquery.Client(credentials=credentials, project=credentials.project_id)

#         query = f"""
#         SELECT 
#             tt.signature, 
#             tt.block_timestamp,
#             tt.pre_token_balances,
#             tt.post_token_balances,
#             tt.accounts
#         FROM 
#             `bigquery-public-data.crypto_solana_mainnet_us.Transactions` AS tt
#         WHERE 
#             EXISTS (
#                 SELECT 1
#                 FROM UNNEST(tt.accounts) AS account
#                 WHERE account.pubkey = '{contract_address}'  
#             )
#             AND tt.block_timestamp BETWEEN '{fromDateTime}' AND '{toDateTime}'
#             AND tt.status = 'Success'
#         ORDER BY 
#             tt.block_timestamp DESC;
#         """

#         query_job = client.query(query)  # Start the query
#         job_id = query_job.job_id  # Get job_id to allow cancelation

#         # Setup a background thread to monitor or handle cancellation
#         cancel_thread = threading.Thread(target=cancel_bigquery_job, args=(client, job_id))
#         cancel_thread.start()

#         # Wait for the query to complete or be cancelled
#         results = query_job.result()  # This will block until the job completes or is canceled

#         if results.total_rows > 0:
#             try:
#                 print(f"Found {results.total_rows} transactions for wallet: {contract_address}")

#                 from_signature = results[0].signature
#                 from_block_timestamp = results[0].block_timestamp
#                 to_signature = results[-1].signature
#                 to_block_timestamp = results[-1].block_timestamp

#                 coin_data = {
#                     "ticker": ticker,
#                     "contract_address": contract_address,
#                     "searched_from_date_time": fromDateTime,
#                     "searched_to_date_time": toDateTime,
#                     "from_signature": from_signature,
#                     "to_signature": to_signature,
#                     "from_block_timestamp": from_block_timestamp,
#                     "to_block_timestamp": to_block_timestamp,
#                     "low_value": low_value,
#                     "peak_value": peak_value,
#                     "discription": discription,
#                     "priority": priority,
#                     "data": results
#                 }

#                 main_folder = 'bigquery_data'
#                 subfolders = ["pending_database", "added_database", "backup_data"]

#                 if not os.path.exists(main_folder):
#                     print("bigquery_data main folder does not exist, creating it...")
#                     os.makedirs(main_folder)

#                 def create_folders(folders):
#                     for folder in folders:
#                         folder_path = os.path.join(main_folder, folder)
#                         if not os.path.exists(folder_path):
#                             print(f"Creating folder: {folder_path}...")
#                             os.makedirs(folder_path)

#                 create_folders(subfolders)

#                 file_name = f"{contract_address}_{from_block_timestamp}_to_{to_block_timestamp}.json"
#                 backup_data_file_path = os.path.join(main_folder, "backup_data", file_name)
#                 pending_database_file_path = os.path.join(main_folder, "pending_database", file_name)

#                 def write_to_json(file_path, data):
#                     try:
#                         with open(file_path, 'w') as json_file:
#                             json.dump(data, json_file, indent=4)
#                         print(f"Data has been written to {file_path}")
#                     except Exception as e:
#                         print(f"Error writing to {file_path}: {e}")

#                 write_to_json(backup_data_file_path, coin_data)
#                 write_to_json(pending_database_file_path, coin_data)

#                 print(f"Data has been written to {backup_data_file_path}")

#                 message = "Successful - json file added to the pending folder"
#                 return True, message

#             except Exception as e:
#                 print(e)
#                 message = "Error - json file did not add to any folder"
#                 return False, message
#         else:
#             message = "No data found (Zero data from BigQuery)."
#             return False, message

#     except Exception as e:
#         print(e)
#         message = "Unknown error happened while requesting BigQuery. Please check login credentials."
#         return False, message






















# import requests
# from flask import flash
# from website.modles import Credentials
# from google.cloud import bigquery
# from google.oauth2 import service_account
# from datetime import datetime
# from decimal import Decimal
# import os
# import json




# def get_transactions_from_Date_and_Time(contract_address,ticker,fromDateTime, toDateTime,set_number , low_value, peak_value,discription,priority
#     ):
#     try :
#         contract_address=contract_address
#         ticker = ticker
#         fromDateTime =fromDateTime
#         toDateTime = toDateTime
#         set_number = set_number

#         ##################################
#         if not os.path.exists("credential_folder"):
#                     print("credential_folder  does not exist, creating it...")
#                     os.makedirs("credential_folder")
#                     message= "Error - No credential file founds.Add it"
#                     return False , message


#         credential_file = Credentials.get_last_item().credentil_file_name

#         if not credential_file:
#             message= "Error - No credential file founds. Add it"
#             return False, message
#         # Replace with the path to your service account key file
#         key_path = os.path.join("credential_folder", credential_file)

#         # Set up credentials using the service account key
#         credentials = service_account.Credentials.from_service_account_file(key_path)

#         # Initialize BigQuery client with the credentials
#         client = bigquery.Client(credentials=credentials, project=credentials.project_id)

#         # for Transactions

#         query = f"""
#         SELECT 
#             tt.signature,  -- Transaction signature (unique transaction ID)
#             tt.block_timestamp
#             tt.pre_token_balances,
#             tt.post_token_balances,
#             tt.accounts
            
#         FROM 
#             `bigquery-public-data.crypto_solana_mainnet_us.Transactions` AS tt
#         WHERE 
#             EXISTS (
#                 SELECT 1
#                 FROM UNNEST(tt.accounts) AS account
#                 WHERE account.pubkey = '{contract_address}'  -- Check if wallet address is involved
#             )
#             AND tt.block_timestamp BETWEEN '{fromDateTime}' AND '{toDateTime}' -- Define your desired time period
#             AND tt.status =  'Success'
            
#         ORDER BY 
#             tt.block_timestamp DESC;
#         """

#         query_job = client.query(query)

#         # Fetch and print the results
#         results = query_job.result()  # Wait for the query to complete

#         # Check if there are results
#         if results.total_rows > 0:
#             try:
#                 print(f"Found {results.total_rows} transactions for wallet: {contract_address}")

#                 from_signature = results[0].signature
#                 from_block_timestamp = results[0].block_timestamp
#                 to_signature = results[-1].signature
#                 to_block_timestamp = results[-1].block_timestamp

#                 coin_data = {
#                     "ticker": ticker,
#                     "contract_address": contract_address,
#                     "searched_from_date_time": fromDateTime,
#                     "searched_to_date_time": toDateTime,
#                     "from_signature": from_signature,
#                     "to_signature": to_signature,
#                     "from_block_timestamp": from_block_timestamp,
#                     "to_block_timestamp": to_block_timestamp,
#                     "from_signature": from_signature,
#                     "to_signature": to_signature,
#                     "low_value":low_value,
#                     "peak_value":peak_value,
#                     "discription":discription,
#                     "priority":priority,
#                     "data": results
#                 }
#                 # Main folder and subfolder paths
#                 main_folder = 'bigquery_data'
#                 subfolders = ["pending_database", "added_database", "backup_data"]

#                 # Ensure the main folder exists; if not, create it
#                 if not os.path.exists(main_folder):
#                     print("bigquery_data main folder does not exist, creating it...")
#                     os.makedirs(main_folder)

#                 # Function to create directories if they don't exist
#                 def create_folders(folders):
#                     for folder in folders:
#                         folder_path = os.path.join(main_folder, folder)
#                         if not os.path.exists(folder_path):
#                             print(f"Creating folder: {folder_path}...")
#                             os.makedirs(folder_path)

#                 # Create main folder and subfolders
#                 create_folders(subfolders)

#                 file_name = f"{contract_address}_{from_block_timestamp}_to_{to_block_timestamp}.json"
#                 # Define file paths for backup and pending database JSON files
#                 backup_data_file_path = os.path.join(main_folder, "backup_data", file_name)
#                 pending_database_file_path = os.path.join(main_folder, "pending_database",file_name)

#                 # Function to write data to a JSON file
#                 def write_to_json(file_path, data):
#                     try:
#                         with open(file_path, 'w') as json_file:
#                             json.dump(data, json_file, indent=4)
#                         print(f"Data has been written to {file_path}")
#                     except Exception as e:
#                         print(f"Error writing to {file_path}: {e}")

#                 # Write data to the specified JSON files
#                 write_to_json(backup_data_file_path, coin_data)
#                 write_to_json(pending_database_file_path, coin_data)

#                 print(f"Data has been written to {backup_data_file_path}")

#                 message= "Sussesfull - json file added to the pending folder"
#                 return True, message
            
#             except Exception as e:
#                 try:

#                     if not os.path.exists("backup_data"):
#                         print("backup_data folder does not exist, creating it...")
#                         os.makedirs("backup_data")

#                     final_backup = os.path.join("backup_data", 'sample1.json')
#                     write_to_json(final_backup, coin_data)

#                     message= "Error - json file did not add to the backup_data"
#                     return False
#                 except Exception as e:
#                     print(e)
#                     message= "Error - json file did not add to any folder"
#                     return False
                 
#         else:
#             message= "WRONG SIGNATURE or DateaTime (Zero data from sql - zero)"
#             return False, message
        
        
#     except Exception as e:
#             print(e)
#             message= "Unknown ERROR happened while requesting Bigquery\n\n check login credentials"+ str(e)
#             return False, message
# #################################




        
# #         base_url = f"https://api.helius.xyz/v0/addresses/{contract_address}/transactions?api-key={halius_api_key}"
# #         all_txn_count=0
# #         valid_txn_count=0
# #         set_number= set_number
# #         current_signature = to_signature
# #         current_timestamp = 0
# #         request_count=0
# #         error_count=0
# #         sucsess_count=0
# #         while True:
# #             running_stop_status=  FinderRunningBreak.get_item(1).running_status
        
# #             if running_stop_status:   ## if running status true it progress will break
# #                 # Cleanup and exit
# #                 flash("Finding was STOP sucessfully",'message')
# #                 message = "Task was stopped."
# #                 if all_txn_count >1:
# #                     print(valid_txn_count)
# #                     AvailableCoinSets.update_txn_count(set_number,valid_txn_count)
# #                 return False, message
# #             if from_signature == "none" or from_signature == "None"  :
# #                 url = base_url +f"&before={to_signature}"
# #             else:
# #                 url = base_url + f"&before={to_signature}"+ f"&until={from_signature}"

# #             response = requests.get(url)
# #             transactions_data = response.json()
# #             request_count=request_count+1
# #             print(request_count)
# #             print(len(transactions_data))

# #             if 'error' in transactions_data:
# #                 if transactions_data['error']=="Endpoint request timed out":
# #                     print("Error count -",error_count)
# #                     if error_count>5 :
# #                         message = transactions_data['error']
# #                         error_count=0
# #                         return False,message
# #                     continue
# #                 if valid_txn_count == 0:

# #                     error_message = transactions_data['error']
# #                     return False, error_message

# #                 else:
# #                     error_message = transactions_data['error']
# #                     message = error_message + "/ Partially Data Taken and error Happened (check_api_key_expired, internet connection) /" + f"Last Signture - {to_signature}"

# #                     item = AvailableCoinSets.get_item(set_number)
# #                     item.current_signature = current_signature
# #                     item.from_timestamp = current_timestamp
# #                     item.tx_count = all_txn_count
# #                     db.session.commit()
# #                     return False, message
                    
                   
# #                     #return(False,error_message + "/ Partially Data Taken and error Happened /" + f"Last Signture - {to_signature}")
# #             if transactions_data and len(transactions_data) > 0:
# #                 error_count=0
# #                 sucsess_count=0
# #                 for txn in transactions_data:
# #                     all_txn_count=all_txn_count+1

# #                     details=getSwappedTransactionDetails(txn, ticker)
    
# #                     if details:
# #                                 # type database adding code
# #                         status = CoinTransactions.add_new_transaction(txn,set_number,details)

# #                         if status :
# #                             valid_txn_count=valid_txn_count+1
# #                             if valid_txn_count%1000==0 :
# #                                 print(valid_txn_count)

# #                             if valid_txn_count==1:
# #                                 new_coin = AvailableCoinSets (
# #                                         set_number= set_number ,
# #                                         contract_address=contract_address,
# #                                         ticker = ticker,
# #                                         discription = discription,
# #                                         priority = priority,
# #                                         from_timestamp = txn['timestamp'],
# #                                         to_timestamp = txn['timestamp'],
# #                                         from_signature = from_signature,
# #                                         current_signature = txn['signature'],
# #                                         to_signature = to_signature,
# #                                         low_value= low_value,
# #                                         peak_value= peak_value,
# #                                         status = 0
# #                                 )
# #                                 try:
# #                                     db.session.add(new_coin)
# #                                     db.session.commit()
# #                                 except Exception as e:
# #                                     db.session.rollback()
# #                                     CoinTransactions.delete_items(set_number)
# #                                     db.session.commit()
# #                                     message = "Only one transaction was added to the data table and it is deleted by the code , Check the database connection (finTransactions.py(line 97))."
# #                                     return False, message
# #                         else:
# #                             if valid_txn_count > 1:
                                
# #                                 item = AvailableCoinSets.query.get(set_number)
# #                                 item.current_signature = txn['signature']
# #                                 item.from_timestamp = txn['timestamp']
# #                                 item.tx_count = all_txn_count -1

# #                                 db.session.commit()
# #                                 message =  "/ Partially Data Taken and error Happened (check database connection) /" + f"Last Signture - {current_signature}"

# #                                 return False, message
            
# #                             else:
# #                                 message = "NO DATA ADDED TO DATABASE"
# #                                 return False, message              
                            
# #                 current_signature = transactions_data[-1]['signature']
# #                 current_timestamp =transactions_data[-1]['timestamp']
# #                 to_signature =current_signature
# #             elif all_txn_count==0:
# #                 print ("Incorrect wallet address or signatures")
# #                 message ="Incorrect wallet address or signatures"
# #                 return False, message
# #             else :
# #                 if valid_txn_count >0 :
# #                     if sucsess_count < 2:
# #                         print(sucsess_count)
# #                         sucsess_count=sucsess_count+1
# #                         continue
# #                     item = AvailableCoinSets.query.get(set_number)
# #                     item.current_signature = current_signature
# #                     item.tx_count = all_txn_count
# #                     item.from_timestamp = current_timestamp
# #                     item.status = 1
# #                     db.session.commit()
# #                     message =f"Sucsess (Number of transactions - {all_txn_count} , Number of valid transactions - {valid_txn_count} )"       
# #                     return True, message
# #                 else:
# #                     message ="Error Happening all txn count > 0 but valid txn count = 0"
# #                     return False, message
                
                
    
# #     except Exception as e:
# #             print ("finderTransaction.py (line 157) - "+ str(e))
# #             check = AvailableCoinSets.check_set_number_exists(set_number)
# #             if check:
# #                     item = AvailableCoinSets.get_item(set_number)
# #                     item.current_signature = current_signature
# #                     item.from_timestamp = current_timestamp
# #                     item.tx_count = all_txn_count
# #                     db.session.commit()
            
# #             message= "WRONG SIGNATURE or Unknown ERROR happened"+ str(e)
# #             return False, message
    

        
# # def getSwappedTransactionDetails(tx, ticker):

# #     description = tx["description"]
# #     transaction_details = {}
# #     try:
# #         if ticker in description:
            
# #             split_description = description.split()
            
# #             if len(split_description) >= 7:
# #                 transaction_details['payee'] = split_description[0].strip()
# #                 transaction_details['action'] = split_description[1].strip()
# #                 transaction_details['sold_amount'] = float(split_description[2])
# #                 transaction_details['sold_token'] = split_description[3].strip()
# #                 transaction_details['got_amount'] = float(split_description[5])
# #                 transaction_details['got_token'] = split_description[6].strip()
                
                
# #                 if split_description[3].strip().upper() == ticker.upper():
# #                     transaction_details['status'] = "sell"
# #                 elif split_description[6].strip().upper() == ticker.upper():
# #                     transaction_details['status'] = "buy"
# #                 else:
# #                     transaction_details['status'] = "no"
# #         return transaction_details
# #     except Exception as e:
# #         print (description)
# #         # Optionally log the error or print it for debugging
# #         print(f"Error processing transaction in (findTransactions.py line 191): {e}")
# #         return transaction_details

    
    




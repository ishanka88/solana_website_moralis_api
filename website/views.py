
from flask import Blueprint, render_template, request, flash, jsonify, send_file
from website.methods import findTransactions, gainersMethods ,whalesCa, pairs,coinFiles,getWhalseData,getInsidersData
from datetime import datetime 
from website.modles import db,AvailableCoinSets, CoinTransactions ,Pairs,Gainers,BackupFolder,MoralisApiKey
import zipfile
from website import db
import pandas as pd
import io
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask import send_file
import logging
from sqlalchemy import inspect
from config import Config





views = Blueprint('views', __name__)



# def status_data():
#     active_coin_count=AvailableCoinSets.get_coins_count_by_status(2)
#     pending_coin_count=AvailableCoinSets.get_coins_count_by_status(1)
#     running_coin_count=AvailableCoinSets.get_coins_count_by_status(0)
#     active_set_count=AvailableCoinSets.get_sets_count_by_status(2)
#     pending_set_count=AvailableCoinSets.get_sets_count_by_status(1)
#     running_set_count=AvailableCoinSets.get_sets_count_by_status(0)


#     return status

###########################################################################################################################################
#################################################################################################################################
## HOME PAGE

# Home
@views.route('/')
def home():
    return render_template("home.html")

#############################################################################################################################################
###################################################################################################################################

## FINDER PAGE

## finder
@views.route('/finder')
def finder():

    def sample_data():
        # sample data
        sample_data_sets = [
        {
            "ticker": "BTC",
            "contract_address": "3B5wuUrMEi5yATD7on46hKfej3pfmd7t1RKgrsN3pump",
            "fromDate": "2024-01-01 12:25:00",
            "toDate": "2024-12-31 23:59:59",
            "from_signature": "0xabcdef1234567890abcdef1234567890abcdef12",
            "to_signature": "0x1234567890abcdef1234567890abcdef12345678",
            "from_block_timestamp": 1611234567,
            "to_block_timestamp": 1612345678,
            "low_value": 500.75,
            "peak_value": 70000.50,
            "description": "Bitcoin transactions over the year 2024",
            "priority": "buy",
            "txns": 100000,
            "file_name": "bquxjob_2d415c27_1936313d570.json",
            "status": 0
        }]

        # {
        #     "ticker": "ETH",
        #     "contract_address": "0x456def...",
        #     "fromDate": "2024-02-01 12:15:45",
        #     "toDate": "2024-02-02 18:30:00",
        #     "from_signature": "0xdef456",
        #     "to_signature": "0xghi789",
        #     "from_block_timestamp": 1675113600,
        #     "to_block_timestamp": 1675117200,
        #     "low_value": 200,
        #     "peak_value": 400,
        #     "description": "Sample transaction for ETH",
        #     "priority": "sell",
        #     "txns": 10,
        #     "file_name": "coin_transaction_data_eth.json",
        #     "flag": 0
        # },
        # {
        #     "ticker": "XRP",
        #     "contract_address": "0x789ghi...",
        #     "fromDate": "2024-03-01 09:00:00",
        #     "toDate": "2024-03-02 20:15:30",
        #     "from_signature": "0xghi789",
        #     "to_signature": "0xjkl012",
        #     "from_block_timestamp": 1677705600,
        #     "to_block_timestamp": 1677709200,
        #     "low_value": 50,
        #     "peak_value": 150,
        #     "description": "Sample transaction for XRP",
        #     "priority": "buy",
        #     "txns": 20,
        #     "file_name": "coin_transaction_data_xrp.json",
        #     "flag": 0
        # }
        # ]
        

        for data in sample_data_sets:
            BackupFolder.add_record(
                data["ticker"],
                data["contract_address"],
                data["fromDate"],
                data["toDate"],
                data["from_signature"],
                data["to_signature"],
                data["from_block_timestamp"],
                data["to_block_timestamp"],
                data["low_value"],
                data["peak_value"],
                data["description"],
                data["priority"],
                data["txns"],
                data["file_name"],
                0  # The flag is set to 0 in this case
            )

    # sample_data()

    return render_template("finder.html")


@views.route('/start-finding', methods=['POST'])
def start_task():

    data = request.get_json()

    contractAddress =data.get('contractAddress')
    fromDate=data.get('fromDate')
    fromHour=data.get('fromHour')
    fromMinute=data.get('fromMinute')
    fromSecond=data.get('fromSecond')
    toDate=data.get('toDate')
    toHour=data.get('toHour')
    toMinute=data.get('toMinute')
    toSecond=data.get('toSecond')
    priority=data.get('priority')
    ticker =data.get('ticker')
    lowValue=data.get('lowValue')
    description=data.get('description')
    peakValue=data.get('peakValue')
    category_index=int(data.get('category'))


    # Create a datetime object for the start date
    fromDate_str = fromDate  # '2024-12-18'
    start_date = datetime.strptime(fromDate_str, "%Y-%m-%d")
    # Create a timedelta object to add the time (hour, minute, second)
    start_time_to_add = timedelta(hours=fromHour, minutes=fromMinute, seconds=fromSecond)
    # Combine the date and time
    formatted_start_date = start_date + start_time_to_add
    # Format the datetime object in the desired format
    formatted_start_date_str = formatted_start_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")


    toDate_str = toDate
    start_date = datetime.strptime(toDate_str, "%Y-%m-%d")
    # Create a timedelta object
    start_time_to_add = timedelta(hours=toHour, minutes=toMinute, seconds=toSecond)
    formatted_end_date = start_date + start_time_to_add
    formatted_end_date_str = formatted_end_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")


    result =findTransactions.get_transactions_from_Date_and_Time(contractAddress,ticker,formatted_start_date_str,formatted_end_date_str, lowValue, peakValue, description,priority,category_index)
    
    return jsonify(result)

    # # Define the time window start_date_time_to_add(optional)
    # start_date = datetime(2024, 11, 24, 18, 50, 0)  # (Year, Month, Day, Hour, Minute, Second)

    # # Define the end date and time (e.g., 15th November 2024 at 6:00 PM)
    # end_date = datetime(2024, 11, 24, 18, 52, 0)  # (Year, Month, Day, Hour, Minute, Second)
    # responce = findTransactions.get_transactions_from_Date_and_Time(ticker,start_date,end_date)



# Route to stop the task (Cancel the running BigQuery job)
@views.route('/stop-finding', methods=['POST'])
def stop_task():
    try:
        Config.SHOULD_STOP = True
    except Exception as e:
        message ="Error - Stopping unsuccessful"
        print (message)
        flash (message,'error')
        flash (f"{str(e)}")




@views.route('/get-pending-coin-set-data-list', methods=['GET'])
def get_pending_coin_data():

    pending_sets = BackupFolder.get_all_sets_in_pending_folder()
    return jsonify(pending_sets)

@views.route('/add-or-delete-prnding-folder-data', methods=['POST'])
def add_or_delete_prnding_folder_data():

    data = request.get_json()  # Get JSON payload
    action = data.get('action')
    rowId = data.get('rowId')
    file_path = BackupFolder.get_file_path_by_id(rowId)
    if not file_path[0]:
        return jsonify(False,file_path[1]), 200

    if action == "add":
        response = coinFiles.addFromPendingFolder(file_path[1],rowId)
        if response[0]:
            BackupFolder.update_status_by_id(rowId,2)
        
        return jsonify(response), 200
  
    elif action=="delete":
        response = coinFiles.deleteFromPendingFolder(file_path[1])
        if response[0]:
            BackupFolder.update_status_by_id(rowId,3)
        
        return jsonify(response), 200

    else:
        return jsonify(False,"Error - Front end Error"), 200




@views.route('/get-data', methods=['GET'])
def get_data():

    active_coin_count=AvailableCoinSets.get_coins_count_by_status(2)
    pending_coin_count=AvailableCoinSets.get_coins_count_by_status(1)
    running_coin_count=AvailableCoinSets.get_coins_count_by_status(0)
    active_set_count=AvailableCoinSets.get_sets_count_by_status(2)
    pending_set_count=AvailableCoinSets.get_sets_count_by_status(1)
    running_set_count=AvailableCoinSets.get_sets_count_by_status(0)

    status_data ={
                "active_coin_count": active_coin_count,
                "pending_coin_count": pending_coin_count,
                "running_coin_count": running_coin_count,
                "active_set_count": active_set_count,
                "pending_set_count": pending_set_count,
                "running_set_count": running_set_count,
            }
    
    ## update transaction and unique wallets count

    # unique_fee_payers_count=CoinTransactions.get_unique_fee_payers_count_by_set_number(1)
    # txn_count=CoinTransactions.get_signatures_count(1)
    # result1=AvailableCoinSets.update_unique_fee_payers_count(1,unique_fee_payers_count)
    # result2=AvailableCoinSets.update_txn_count(1,txn_count)

    # print(result2)
    # print(result1)


    coins_count = AvailableCoinSets.get_coins_count()
    set_counts= AvailableCoinSets.get_max_set_number()
    info={'coins_count':coins_count,'set_counts':set_counts}
    status = request.args.get('status')
    data = process_data_based_on_status(status)

    return jsonify({'data': data,'coins_count':coins_count,'set_counts':set_counts, 'status_data': status_data})  # Wrap the data in a dictionary with key 'data'

def process_data_based_on_status(status):
    # Convert status string to corresponding integer value
    if status == "running":
        status_value = 0
    elif status == "pending":
        status_value = 1
    else:
        status_value = 2

    coins_data = AvailableCoinSets.get_coins_sets_by_status(status_value)
    
    # Convert the transactions to a list of dictionaries
    transactions_data = []
    for coin in coins_data:
        if coin.low_value != 0:
                profit = round((coin.peak_value - coin.low_value) * 100 / coin.low_value)
        else:
                profit = 0  # Or some other value indicating undefined profit


        from_dt = datetime.strptime(coin.from_timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
        # Format to desired output
        from_date = from_dt.strftime('%Y-%m-%d %H:%M:%S UTC')

        to_dt = datetime.strptime(coin.to_timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
        # Format to desired output
        to_date = to_dt.strftime('%Y-%m-%d %H:%M:%S UTC')

        valid_tx_count = coin.tx_count - coin.fake_transactions_count
        
        transactions_data.append({
            'set_number': coin.set_number,
            'ticker': coin.ticker,
            'priority':coin.priority,
            'description': coin.description,
            'from_date': from_date,
            'to_date': to_date,
            'txn_count': coin.tx_count,
            'valid_txn_count': valid_tx_count,
            'uni_wallets_count': coin.uni_wallet_count,
            'buy_uni_wallet_count': coin.buy_uni_wallet_count,
            'sell_uni_wallet_count':coin.sell_uni_wallet_count,
            'status': coin.status,
            'to_signature': coin.to_signature,
            'from_signature': coin.from_signature,
            'contract_adress': coin.contract_address,
            'profit' : profit,
            'category_index' : coin.category_index

            
        })
    return transactions_data

##############################################

@views.route('/table', methods=['GET'])
def action():
    action = request.args.get('action')
    set_number = request.args.get('element_id')
    response = findAction(action, set_number)
    return jsonify({'data': response[0], 'action':response[1],'status': response[2]})  # Removed trailing comma

def findAction(action, set_number):
    try:
        if action == "delete":
            update = CoinTransactions.delete_items(set_number)
            if update:
                check=Pairs.is_set_number_in_pairs(set_number)
                if check :
                    Pairs.delete_pairs_which_include_set_number(set_number)
                update = AvailableCoinSets.delete_item(set_number)
                if update:
                    responce_one=BackupFolder.get_row_id_from_set_number(set_number)
                    if not responce_one[0]:
                        return update,action, responce_one[1]
                    row = responce_one[1]
                    file_path = row.file_name
                    response = coinFiles.deleteFromAddedFolder(file_path)
                    if response[0]:
                        row_id =row.id
                        BackupFolder.update_status_by_id(row_id,3)
                        BackupFolder.update_set_number_by_id(row_id,0)
                        return update, action, "Delete Sucsess" 
                    return update, action, "No row available" 
                else:
                    return update, action, "Try again - All Transactions Deleted but Coin not deleted in database"
            else:
                return update, action,"Error - Try again"

        if action == "info":
            data = AvailableCoinSets.get_item(set_number)
            coin_data = []
            coin_data.append({
                'set_number': data.set_number,
                'contract_address': data.contract_address,
                'ticker': data.ticker,
                'priority':data.priority,
                'description': data.description,
                'low_value':data.low_value,
                'peak_value': data.peak_value,
                'from_timestamp': data.from_timestamp,
                'to_timestamp': data.to_timestamp,
                'from_signature': data.from_signature,
                'current_signature': data.current_signature,
                'to_signature': data.to_signature,
                'txn_count': data.tx_count,
                'valid_tx_count': data.valid_tx_count,
                'uni_wallets_count': data.uni_wallet_count,
                'status': data.status
            })
            return coin_data, action, "Done"
        if action == "pending-to-active":
            update=AvailableCoinSets.update_status(set_number,2) ## 2-active
            if update:
                getWhalseData.getWhales()
                getInsidersData.getInsiders()
                return update, action, "Sucsess"
            else:
                return update, action, "Error -Update Unsuccesfull"
            
        if action == "active-to-pending":
            update=AvailableCoinSets.update_status(set_number,1) ## 1-pending
            if update:
                getWhalseData.getWhales()
                getInsidersData.getInsiders()
                return update, action, "Sucsess" 
            else:
                return update, action, "Error - Update Unsuccesfull- try again"
        
        if action == "running-to-pending":
            update=AvailableCoinSets.update_status(set_number,1) ## 1-pending
            if update:
                return update, action, "Sucsess" 
            else:
                return update, action, "Error - Update Unsuccesfull- try again"
            
    except Exception as e:
        print (str(e))

###########################################

@views.route('/api_value', methods=['GET'])
def getApi():
    action = request.args.get('action')
    new_api_key = request.args.get('api_key')
    current_api = MoralisApiKey.get_last_item()
    ## take api key to show in ui
    if action == "get":

        if current_api :
            return jsonify({'data': current_api.api_key}) 
        else:
            return jsonify({'data': "Null"}) 

    if action == "add" :
        response =MoralisApiKey.add_api(new_api_key)
        if response :
            return jsonify({'data': new_api_key})
        else :
            flash("Error- failed to add")
            return jsonify({'data': current_api.api_key}) 


###############################################################

@views.route('/merge', methods=['GET'])
def mergeApi():
    set1 = request.args.get('set1')
    set2 = request.args.get('set2')

    if not set1 or not set2:
        return jsonify({'status': False, 'message': 'Both set1 and set2 must be provided.'}), 400

    try:
        check1 = AvailableCoinSets.check_set_number_exists(set1)
        check2 = AvailableCoinSets.check_set_number_exists(set2)

        if not check1 and not check2 :
            return jsonify({'status': False, 'message': 'One or both Set numbers are not in database'}), 404


        priority1= AvailableCoinSets.get_priority(set1)
        priority2= AvailableCoinSets.get_priority(set2)

        if priority1 != priority2:
             return jsonify({'status': False, 'message': 'One or both Set numbers are not in database'}), 404

    

        # Fetch items from the data source (e.g., database or dictionary)
        set1_ca = AvailableCoinSets.get_item(set1).contract_address
        set2_ca = AvailableCoinSets.get_item(set2).contract_address

        # Compare the fetched items
        if set1_ca and set2_ca and set1_ca == set2_ca:
            CoinTransactions.update_transaction_set_number (set1,set2)

            set1_txn_count=AvailableCoinSets.get_txn_count(set1)
            set2_txn_count=AvailableCoinSets.get_txn_count(set2)
            total_txn_count= set1_txn_count + set2_txn_count

            result1 = AvailableCoinSets.update_txn_count(set1,total_txn_count)
            if not result1:
                return jsonify({'status': False, 'message': 'txn count is not updated'}), 404
    
            AvailableCoinSets.delete_item(set2)

            updateApi()
            return jsonify({'status': True, 'message': 'Merge Success'}), 200


    except Exception as e:

        # Log the exception for debugging purposes
        print(f"An error occurred: {e}")
        return jsonify({'status': False, 'message': 'An error occurred while processing the request.'}), 500

   

##################################################

@views.route('/update', methods=['GET'])
def updateApi():
    ## update transaction and unique wallets count
    try:
        set_num_list = AvailableCoinSets.get_all_set_numbers()
        for set in set_num_list:
            current_signature = CoinTransactions.get_last_signature(set)
            valid_txn_count=CoinTransactions.get_signatures_count(set)
            buy_txn_count=CoinTransactions.get_buy_txn_count(set)
            sell_txn_count=CoinTransactions.get_sell_txn_count(set)
            unique_fee_payers_count=CoinTransactions.get_unique_fee_payers_count_by_set_number(set)
            unique_buy_fee_payers_count = CoinTransactions.get_sell_or_buy_unique_fee_payers_count_by_set_number(set,"buy")
            unique_sell_fee_payers_count = CoinTransactions.get_sell_or_buy_unique_fee_payers_count_by_set_number(set,"sell")

            AvailableCoinSets.update_current_signature(set,current_signature)
            AvailableCoinSets.update_valid_txn_count(set,valid_txn_count)
            AvailableCoinSets.update_buy_txn_count(set,buy_txn_count)
            AvailableCoinSets.update_sell_txn_count(set,sell_txn_count)
            AvailableCoinSets.update_unique_fee_payers_count(set,unique_fee_payers_count)
            AvailableCoinSets.update_buy_unique_fee_payers_count(set,unique_buy_fee_payers_count)
            AvailableCoinSets.update_sell_unique_fee_payers_count(set,unique_sell_fee_payers_count)

        return jsonify({'status': True})
    except:
        return jsonify({'status': False})
    

###########################################

@views.route('/import-data', methods=['POST'])
def import_data():
    # Check if the request contains files
    if 'files' not in request.files:
        return jsonify({"error": "No files provided"}), 400

    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No files provided"}), 400

    # Loop through uploaded files
    for file in files:
        if file.filename.endswith('.csv'):
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file)
            
            # Get table name from file name or other logic
            table_name = file.filename.replace('.csv', '')

            # Check if table exists
            if table_name in inspect(db.engine).get_table_names():
                # Insert data into the database
                df.to_sql(table_name, db.engine, if_exists='replace', index=False)
            else:
                return jsonify({"error": f"Table {table_name} does not exist"}), 400

    return jsonify({"message": "Data imported successfully"}), 200

############################################

logging.basicConfig(level=logging.DEBUG)

@views.route('/export-data', methods=['GET'])
def export_data():

    try:
        # Create a dictionary to store CSV buffers for each table
        csv_buffers = {}

        # Get the table names from the database
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        # Loop through each table and export it to a CSV buffer
        for table_name in tables:
            # Read the table into a Pandas DataFrame
            df = pd.read_sql_table(table_name, db.engine)
            
            # Create an in-memory string buffer
            csv_buffer = io.StringIO()
            # Write the DataFrame to the CSV buffer (without the index)
            df.to_csv(csv_buffer, index=False)
            # Move the pointer back to the beginning of the buffer
            csv_buffer.seek(0)
            
            # Store the buffer in the dictionary
            csv_buffers[table_name] = csv_buffer

        # Create an in-memory ZIP buffer
        zip_buffer = io.BytesIO()

        # Write each table's CSV buffer into the ZIP file
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for table_name, csv_buffer in csv_buffers.items():
                zip_file.writestr(f"{table_name}.csv", csv_buffer.getvalue())

        # Move the pointer of the zip buffer back to the start
        zip_buffer.seek(0)

        # Send the ZIP file containing all CSVs as an attachment
        return send_file(
            zip_buffer,
            as_attachment=True,
            download_name='exported_data.zip',
            mimetype='application/zip'
        )

    except Exception as e:
        # Log the error and return a response
        logging.error(f"Error while exporting data to CSV: {e}")
        return jsonify({"error": "An error occurred while exporting data."}), 500


#############################################################


@views.route('/get-transactions-data', methods=['GET'])
def getTransactionsDetails():
    try:
        # Get 'setNumber' from the request's query parameters
        setNumber = request.args.get('setNumber')

        # Convert setNumber to integer, handling the case when it's not a valid number
        try:
            setNumber = int(setNumber)
        except ValueError:
            return jsonify({'status': False, 'message': 'Invalid setNumber value'}), 400

        # Fetch transactions by setNumber using the class method
        transactions = CoinTransactions.get_transactions_by_set_number(setNumber)

        # Check if transactions exist
        if transactions:
            # Convert transactions to list of dictionaries
            transaction_list = [transaction.to_dict() for transaction in transactions]
            return jsonify({'status': True, 'transactions': transaction_list})
        else:
            return jsonify({'status': False, 'message': 'No transactions found for the given setNumber'}), 404

    except Exception as e:
        # Print or log the error message for debugging purposes
        print(f"Error: {e}")
        return jsonify({'status': False, 'message': 'An error occurred while processing your request'}), 500



###############################################################################################
###############################################################################################

## WHALES PAGE

@views.route('/whales', methods=['GET', 'POST'])
def whale():
        if Config.WHALE_PAGE_MAIN_TABLE_DATA==None:
            getWhalseData.getWhales()

        return render_template("whales.html")

##whales
@views.route('/get-whales-data', methods=['GET'])
def whale_data():

    return jsonify(Config.WHALE_PAGE_MAIN_TABLE_DATA )





########################################################################################################################################################
###############################################################################################################################################

## PAIRS PAGE
@views.route('/pairs')
def pairs_page():

    return render_template("pairs.html")


@views.route('/get-pairs-data', methods=['GET'])
def getPairs():
    
    table_one_data=pairs.get_available_pairs()

    # table_one_data= [
    #     {
    #         'contract_asdress': 'Big4MGvf4dgmE6YNKegjcGBTkUvvVoi11Qrdw8BGMKen',
    #         'ticker': 'daddy',
    #         'buy_set_no': 2,
    #         'sell_set_no': 1
    #     },
    #             {
    #         'contract_asdress': 'Big4MGvf4dgmE6YNKegjcGBTkUvvVoi11Qrdw8BGMKen',
    #         'ticker': 'daddy',
    #         'buy_set_no': 2,
    #         'sell_set_no': 1
    #     },
    #             {
    #         'contract_asdress': 'Big4MGvf4dgmE6YNKegjcGBTkUvvVoi11Qrdw8BGMKen',
    #         'ticker': 'daddy',
    #         'buy_set_no': 2,
    #         'sell_set_no': 1
    #     } 
    # ]

    table_two_data=pairs.get_whales_from_pairs(table_one_data)

    # table_two_data = [
    #         {      
    #         'contract_asdress': 'Big4MGvf4dgmE6YNKegjcGBTkUvvVoi11Qrdw8BGMKen',
    #         'ticker': 'daddy',
    #         'buy_set_no': 2,
    #         'sell_set_no': 1,
    #         'whales': [
	# 	                {'whale_adress': '4Cnk9EPnW5ixfLZatCPJjDB1PUtcRpVVgTQukm9epump'},
	# 	                {'whale_adress': '5Cnk9EPnW5ixfLZatCPJjDB1PUtcRpVVgTQukm9epump'},
    #                 ]
    #         },
		
    #      {   
    #         'contract_asdress': 'kig4MGvf4dgmE6YNKegjcGBTkUvvVoi11Qrdw8BGMKen',
    #         'ticker': 'monkey',
    #         'buy_set_no': 2,
    #         'sell_set_no': 1,
    #         'whales': [
	# 	                {'whale_adress': '100Cnk9EPnW5ixfLZatCPJjDB1PUtcRpVVgTQukm9epump'},
	# 	                {'whale_adress': '22Cnk9EPnW5ixfLZatCPJjDB1PUtcRpVVgTQukm9epump'},
    #                 ]
    #     },
    # ]

    return jsonify({'pairs': table_one_data, 'whales': table_two_data } )

#################################################

@views.route('/set_pair', methods=['GET'])
def setPair():
    set1 = request.args.get('set1')
    set2 = request.args.get('set2')
    description = request.args.get('description')
    try:
        check1 = AvailableCoinSets.check_set_number_exists(set1)
        check2 = AvailableCoinSets.check_set_number_exists(set2)
        if not check1 or not check2:
            return jsonify({'status': False, 'message': 'Invalid SET number (SET number is not in database)'}), 400
        
        check3 = Pairs.check_pair_existence(set1,set2)
        if check3:
            return jsonify({'status': False, 'message': 'This pair is already exist'}), 400
        
        set1_ca = AvailableCoinSets.get_item(set1).contract_address
        set2_ca = AvailableCoinSets.get_item(set2).contract_address
        if set1_ca!=set2_ca :
            return jsonify({'status': False, 'message': 'Error - Sets must be in same coin '}), 400
        
        priority1=AvailableCoinSets.get_priority(set1)
        priority2=AvailableCoinSets.get_priority(set2)

        if priority1==priority2:
            return jsonify({'status': False, 'message': 'Error - Boths sets have same priority '}), 400
            

        result =Pairs.add_pair(set1,set2,description)
        if result:
                return jsonify({'status': True, 'message':"Success"}), 200
        else:
            return jsonify({'status': False, 'message': "Internal Error "}), 400



    except Exception as e:

        # Log the exception for debugging purposes
        print(f"An error occurred: {e}")
        return jsonify({'status': False, 'message': 'An error occurred while processing the request.'}), 500


#################################################

@views.route('/delete_pair', methods=['GET'])
def delete_pair():
    set1 = request.args.get('set1')
    set2 = request.args.get('set2')
    try:
        result =Pairs.delete_pair(set1,set2)
    
        if result:
            return jsonify({'status': True, 'message': 'DELETE SUCCESS'}), 200
        else:
            return jsonify({'status': False, 'message': 'ERROR - DELETE UNSUCCESS'}), 400


    except Exception as e:

        # Log the exception for debugging purposes
        print(f"An error occurred: {e}")
        return jsonify({'status': False, 'message': 'An error occurred while processing the request.'}), 500

   

##############################################################################################
@views.route('/gainers')
def gainers():
    return render_template("gainers.html")


@views.route('/add-gainers', methods=['POST'])
def add_gainers():

        data = request.get_json()
        contractAddress =data.get('contractAddress')
        walletAddress=data.get('walletAddress')
        ticker=data.get('ticker')
        gainedProfit=data.get('gainedProfit')
        result = gainersMethods.addGainers(contractAddress,walletAddress,ticker,gainedProfit)
        return jsonify(result)


@views.route('/get-whale-gainers-data', methods=['GET'])
def get_whale_gainers():
    try:
        gainer_whales_list = Gainers.get_gainers_with_duplicate_wallets()
        return jsonify(gainer_whales_list)
    except Exception as e:
        return jsonify(None, str(e))



###############################################################################################
###############################################################################################

## Insider PAGE

@views.route('/insiders', methods=['GET', 'POST'])
def insiders():
        if Config.INSIDERS_PAGE_MAIN_TABLE_DATA==None:
            getInsidersData.getInsiders()

        return render_template("insiders.html")

##whales
@views.route('/get-insiders-data', methods=['GET'])
def insiders_data():

    return jsonify(Config.INSIDERS_PAGE_MAIN_TABLE_DATA )
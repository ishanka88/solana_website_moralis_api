from website.modles import AvailableCoinSets, CoinTransactions
from flask import flash
from website.methods import findTransactions



def addCoinTransactions(file_all_data):
    try:
        # Extract necessary data from file_all_data (assuming it's a dictionary)
        meme_token_address = file_all_data["contract_address"]

        ticker = file_all_data["ticker"]
        from_signature = file_all_data["from_signature"]
        to_signature = file_all_data["to_signature"]
        low_value = file_all_data["low_value"]
        peak_value = file_all_data["peak_value"]
        description = file_all_data["description"]
        from_block_timestamp = file_all_data["from_block_timestamp"]
        to_block_timestamp = file_all_data["to_block_timestamp"]
        priority = file_all_data["priority"]

        # Access the 'data' attribute (which is a list of transactions)
        data = file_all_data["data"]

        transactions_count = 0
        fake_transactions_count = 0
        buy_transactions_count = 0
        sell_transactions_count = 0

        Transactions_list = []

        max_set_number = AvailableCoinSets.get_max_set_number()  # Get the max set number
        set_number = (max_set_number + 1) if max_set_number is not None else 1  # Increment by 1 or set to 1 if None

        # Process each transaction in data
        for row in data:

            # sample_row ={
            #     "transactionHash": "3tMqiQd6jsh1zAz3dYNpKfeDXthm35i7tvMdVqazAqxAMjjhNtW2r2SiVeRXoVLbxm9cfMyxEGNX2gwWCywf4jJr",
            #     "transactionType": "sell",
            #     "transactionIndex": 468,
            #     "subCategory": "partialSell",
            #     "blockTimestamp": "2024-12-18T00:00:00.000Z",
            #     "blockNumber": 308148058,
            #     "walletAddress": "AdCNnoFcUfyefhyfRWf1jNf8426e88po8AQLbaJtQh7u",
            #     "pairAddress": "78sBWyimVhLumzZg1bdMD6ogGig8QpmgYZqCXNyMxx4z",
            #     "pairLabel": "UFD/SOL",
            #     "exchangeAddress": "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8",
            #     "exchangeName": "Raydium AMM v4",
            #     "exchangeLogo": "https://entities-logos.s3.amazonaws.com/raydium.png",
            #     "baseToken": "eL5fUxj2J4CiQsmW85k5FG9DvuQjjUoBHoQBi2Kpump",
            #     "quoteToken": "So11111111111111111111111111111111111111112",
            #     "bought": {
            #         "address": "So11111111111111111111111111111111111111112",
            #         "name": "Wrapped SOL",
            #         "symbol": "SOL",
            #         "logo": null,
            #         "amount": "2.681047410",
            #         "usdPrice": 223.225410788,
            #         "usdAmount": 598.4779094393535,
            #         "tokenType": "token0"
            #     },
            #     "sold": {
            #         "address": "eL5fUxj2J4CiQsmW85k5FG9DvuQjjUoBHoQBi2Kpump",
            #         "name": "Unicorn Fart Dust",
            #         "symbol": "UFD",
            #         "logo": null,
            #         "amount": "432884.670590000",
            #         "usdPrice": 0.001382534,
            #         "usdAmount": 598.477775169475,
            #         "tokenType": "token1"
            #     },
            #     "baseQuotePrice": "0.000006193443636723822",
            #     "totalValueUsd": 598.477909439
            # }

            transactions_count += 1
            signature = row["transactionHash"]
            fee_payer = row["walletAddress"]
            block_timestamp = row["blockTimestamp"]

            bought_token = row["bought"]["symbol"]
            bought_token_amount = row["bought"]["amount"]

            sold_token = row["sold"]["symbol"]
            sold_token_amount = row["sold"]["amount"]
            
            status = row["transactionType"]
            sub_category = row["subCategory"]

            if bought_token != ticker and sold_token != ticker:
                fake_transactions_count +=1
            
            if bought_token == ticker and sold_token == ticker:
                fake_transactions_count +=1
            



            # Create the CoinTransactions object and append it to the list
            transaction = CoinTransactions(
                signature=signature,
                time_stamp=block_timestamp,
                fee_payer=fee_payer,
                bought_token=bought_token,
                bought_token_amount=bought_token_amount,
                sold_token=sold_token,
                sold_token_amount=sold_token_amount,
                status=status,
                sub_category =sub_category,
                set_number=set_number
            )

            Transactions_list.append(transaction)


        # Add the list of transactions to the database using bulk insert
        response = CoinTransactions.add_transactions_to_db(Transactions_list)
        if response[0]:
            # Fetch counts for unique wallets for each transaction status
            buy_transactions_count = CoinTransactions.get_buy_txn_count(set_number)
            sell_transactions_count = CoinTransactions.get_sell_txn_count(set_number)
            uni_wallet_count = CoinTransactions.get_unique_fee_payers_count_by_set_number(set_number)
            buy_uni_wallet_count = CoinTransactions.get_sell_or_buy_unique_fee_payers_count_by_set_number(set_number, "buy")
            sell_uni_wallet_count = CoinTransactions.get_sell_or_buy_unique_fee_payers_count_by_set_number(set_number, "sell")

            # Prepare the coin set data
            coin_set_data = {
                'set_number': set_number,
                'contract_address': meme_token_address,
                'ticker': ticker,
                'description': description,
                'priority': priority,
                'from_timestamp': from_block_timestamp,
                'to_timestamp': to_block_timestamp,
                'from_signature': from_signature,
                'to_signature': to_signature,
                'tx_count': transactions_count,
                'fake_transactions_count': fake_transactions_count,
                'buy_tx_count': buy_transactions_count,
                'sell_tx_count': sell_transactions_count,
                'uni_wallet_count': uni_wallet_count,
                'buy_uni_wallet_count': buy_uni_wallet_count,
                'sell_uni_wallet_count': sell_uni_wallet_count,
                'low_value': low_value,
                'peak_value': peak_value,
                'status': 1  # Status 1 - pending
            }


            # Add the coin set data to AvailableCoinSets
            result = AvailableCoinSets.add_new_coin_set(coin_set_data)

            if result[0]:
                message = "Coin set added successfully"
                flash(message,'message')
                return True, message, set_number,
            else:
                # Rollback in case of failure to add the coin set
                delete = CoinTransactions.delete_items(set_number)
                if delete:
                    message = "Error - transactions added but Set details not added in AvailableCoinsets, so transactions deleted."
                    return False, message
                else:
                    message = "Error - transactions added but Set details not added, and transactions remain in the CoinTransactions table."
                    return False, message
        else:
            return response

    except Exception as e:
        # Log the error with detailed information
        message = f"Error in addCoinTransactions function: {str(e)}"
        flash(message,'error')
        print(message)
        delete = CoinTransactions.delete_items(set_number)
        if delete:
                return False, message
        else:
                return False, message
 



# from website.modles import AvailableCoinSets,CoinTransactions,Pairs
# from website import db
# from flask import flash
# import os
# import json
# from website.methods import findTransactions, gainersMethods ,whalesCa, pairs,coinFiles
# from decimal import Decimal


# def addCoinTransactions(file_all_data):
    
#     try :
    
#         meme_token_address = file_all_data["contract_address"]
#         ticker = file_all_data["ticker"]
#         from_signature = file_all_data["from_signature"]
#         to_signature = file_all_data["to_signature"]
#         low_value = file_all_data["low_value"]
#         peak_value = file_all_data["peak_value"]
#         discription = file_all_data["discription"]
#         from_block_timestamp = file_all_data["from_block_timestamp"]
#         to_block_timestamp = file_all_data["to_block_timestamp"]
#         priority = file_all_data["priority"]

#         # Access the 'data' attribute (this will be a list in this case)
#         data = file_all_data["data"]

#         transactions_count = 0
#         wallet_transfers_count = 0
#         fake_transactions_count = 0
#         buy_transactions_count = 0
#         sell_transactions_count = 0

#         pre_token_balance = 0.0
#         post_token_balance = 0.0

#         Transactions_list = []
#         set_number = AvailableCoinSets.get_max_set_number() + 1

#         for row in data:
            
#             transactions_count += 1
#             signature = row["signature"]
#             accounts = row["accounts"]
#             block_timestamp = 1111111 # row["block_timestamp"]
#             pre_token_balances = row["pre_token_balances"]
#             post_token_balances = row["post_token_balances"]
           

#             for account in accounts:
#                 if (account["signer"] == "true" and account["writable"]== "false" )or (account["signer"] == True and account["writable"]== False ) :
#                     fee_payer = account["pubkey"]
#                     print(fee_payer)
#                     break
            
#             for balance in pre_token_balances:
#                 if balance["mint"] == meme_token_address and balance["owner"] == fee_payer :
#                     pre_token_balance = balance['amount'] * Decimal(10**-balance['decimals'])
#                     break
            
#             for balance in post_token_balances:
#                 if balance["mint"] == meme_token_address and balance["owner"] == fee_payer :
#                     post_token_balance = balance['amount'] * Decimal(10**-balance['decimals'])
#                     break
#             x=0   
#             for balance in pre_token_balances:
#                 if balance["mint"] != meme_token_address:
#                     x=1
#                     break
           
#             if x==0 :
#                 status= "transfer" 
#                 wallet_transfers_count +=1 

#             elif post_token_balance == pre_token_balance:
#                 status = "fake"
#                 fake_transactions_count +=1
#             elif post_token_balance > pre_token_balance:
#                 status = "buy"
#                 buy_transactions_count += 1
#             else:
#                 status = "sell"
#                 sell_transactions_count +=1


#             transaction = CoinTransactions(
#                 signature=signature,
#                 time_stamp=block_timestamp,  # Assuming the timestamp is the current time
#                 fee_payer=fee_payer ,
#                 pre_token_balance=pre_token_balance,  # Example of how you might calculate sold_amount
#                 post_token_balance=post_token_balance,  # The token sold, here we assume it's the meme token
#                 # got_amount=post_token_balance,  # The amount received in exchange
#                 # got_token="USD",  # Example; you can replace this with the actual token received
#                 status=status,  # Transaction status
#                 set_number= set_number # This is just a placeholder; you'll probably calculate or set this dynamically
#             )

#             Transactions_list.append(transaction)
        
#         response = CoinTransactions.add_transactions_to_db(Transactions_list)
#         if response[0]:
#             uni_wallet_count =CoinTransactions.get_unique_fee_payers_count_by_set_number(set_number)
#             buy_uni_wallet_count = CoinTransactions.get_sell_or_buy_unique_fee_payers_count_by_set_number(set_number,"buy")
#             sell_uni_wallet_count = CoinTransactions.get_sell_or_buy_unique_fee_payers_count_by_set_number(set_number,"sell")

#             coin_set_data = {
#                 'set_number': set_number,
#                 'contract_address': meme_token_address,
#                 'ticker': ticker,
#                 'description': discription,
#                 'priority': priority,
#                 'from_timestamp': from_block_timestamp,
#                 'to_timestamp': to_block_timestamp,
#                 'from_signature': from_signature,
#                 'to_signature': to_signature,
#                 'tx_count': transactions_count,
#                 'fake_transactions_count': fake_transactions_count,
#                 'buy_tx_count': buy_transactions_count,
#                 'sell_tx_count': sell_transactions_count,
#                 'uni_wallet_count': uni_wallet_count,
#                 'buy_uni_wallet_count': buy_uni_wallet_count,
#                 'sell_uni_wallet_count': sell_uni_wallet_count,
#                 'low_value': low_value,
#                 'peak_value': peak_value,
#                 'status': 1  # Status 1 - pending
# }
#             result = AvailableCoinSets.add_new_coin_set(coin_set_data)

#             if result[0]:
#                 message = "Coin set added successfully"
#                 return True, message
#             else :
#                 delete =CoinTransactions.delete_items(set_number)
#                 if delete :
#                     message = "Error - transactions added but Set details not added in AvailableCoinsets, so that all transactions deleted from CoinTransactions table"
#                     return False, message
#                 else :
#                     message = "Error - transactions added but Set details not added in AvailableCoinsets, So now there are transactions data but not i available coins list"
#                     return False, message

#         else:
#             return response

#     except Exception as e :
#         message = "Error - In coinTransactions.py file line 96"
#         print(e)
#         return False, message
#     # 42rqbbTfkVp94sAx6E3tmAW4ZnfcmWq5EK8Yb78Zqet82JvhaJjVichPTns13YqCMGCZE6kZriHCWEULLAXYEVp2
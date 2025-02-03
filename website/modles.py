from flask import flash,jsonify
from website import db
from sqlalchemy.sql import func, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import logging
from collections import defaultdict

class AvailableCoinSets(db.Model): ## searchedCoins

     set_number= db.Column(db.Integer, primary_key=True,nullable=False)
     contract_address=db.Column(db.String(100),nullable=False)
     ticker = db.Column(db.String(150),nullable=False)
     description = db.Column(db.String(150),nullable=False)
     priority = db.Column(db.String(10),nullable=False,default="no")
     from_timestamp = db.Column(db.String(150),nullable=False)
     to_timestamp = db.Column(db.String(150), nullable=False)
     from_signature = db.Column(db.String(100), nullable=False)
     to_signature = db.Column(db.String(100),nullable=False)
     tx_count= db.Column(db.Integer,nullable=False,default=1)
     fake_transactions_count= db.Column(db.Integer,nullable=False,default=0)
     buy_tx_count = db.Column(db.Integer,nullable=False, default=0)
     sell_tx_count = db.Column(db.Integer,nullable=False, default=0)
     uni_wallet_count = db.Column(db.Integer, nullable=False,default=0)
     buy_uni_wallet_count=db.Column(db.Integer, nullable=False,default=0)
     sell_uni_wallet_count=db.Column(db.Integer, nullable=False,default=0)
     low_value = db.Column(db.Float, nullable=False, default=0.0)  # Corrected `defaut` to `default` and added `0.0`
     peak_value = db.Column(db.Float, nullable=False, default=0.0)
     status = db.Column(db.Integer,nullable=False)  ## 0 - running , 1-pending , 2-active




     @staticmethod
     def add_new_coin_set(data):
          """
     Add a new coin set to the AvailableCoinSets table.
     
     :param data: A dictionary containing the coin set data
     :return: True if the transaction is successful, False otherwise
     """
          try:
               # Create a new AvailableCoinSets object with the provided data   
               new_coin_set = AvailableCoinSets(
                    set_number=data['set_number'],
                    contract_address=data['contract_address'],
                    ticker=data['ticker'],
                    description=data['description'],
                    priority=data['priority'],
                    from_timestamp=data['from_timestamp'],
                    to_timestamp=data['to_timestamp'],
                    from_signature=data['from_signature'],
                    to_signature=data['to_signature'],
                    tx_count=data['tx_count'],
                    fake_transactions_count=data['fake_transactions_count'],
                    buy_tx_count=data['buy_tx_count'],
                    sell_tx_count=data['sell_tx_count'],
                    uni_wallet_count=data['uni_wallet_count'],
                    buy_uni_wallet_count=data['buy_uni_wallet_count'],
                    sell_uni_wallet_count=data['sell_uni_wallet_count'],
                    low_value=data['low_value'],
                    peak_value=data['peak_value'],
                    status=data['status']
               )

               # Add the new object to the session and commit
               db.session.add(new_coin_set)
               db.session.commit()

               return True, "Coin set added successfully"
          
          except IntegrityError as e:
               # Handle integrity error (e.g., duplicate entries or violations of NOT NULL constraints)
               db.session.rollback()  # Rollback the session to undo any changes made
               print (str(e))
               return False, f"Integrity error: {str(e)}"
          
          except SQLAlchemyError as e:
               # Catch any other SQLAlchemy-related errors
               db.session.rollback()
               print (str(e))
               return False, f"Database error: {str(e)}"
          
          except Exception as e:
               # Catch any other generic errors
               db.session.rollback()
               print (str(e))
               return False, f"Unexpected error: {str(e)}"

          
        
     @staticmethod
     def get_item(set_num):
        item = AvailableCoinSets.query.get(set_num)
        return item
     def get_priority(set_num):
          priority = AvailableCoinSets.get_item(set_num).priority
          return priority
     
     
     def get_buy_sets_count (contract_address):

          try:
               # Query the database for the count of records with the specified set number
               count = db.session.query(AvailableCoinSets).filter_by(contract_address=contract_address,status=2,priority="buy").count()
               
               # Return the count
               return count
          except SQLAlchemyError as e:
               # Handle database errors
               flash(f"An error occurred: {e}", category='error')
               db.session.rollback()  # Rollback the session in case of error
               return 0
          except Exception as e:
               # Handle any other unexpected errors
               flash(f"An unexpected error occurred: {e}", category='error')
               db.session.rollback()  # Rollback the session in case of error
               return 0
          
     def get_sell_sets_count (contract_address):

          try:
               # Query the database for the count of records with the specified set number
               count = db.session.query(AvailableCoinSets).filter_by(contract_address=contract_address,status=2,priority="sell").count()
               
               # Return the count
               return count
          except SQLAlchemyError as e:
               # Handle database errors
               flash(f"An error occurred: {e}", category='error')
               db.session.rollback()  # Rollback the session in case of error
               return 0
          except Exception as e:
               # Handle any other unexpected errors
               flash(f"An unexpected error occurred: {e}", category='error')
               db.session.rollback()  # Rollback the session in case of error
               return 0
     
     def get_txn_count(set_num):
          try:
               # Query the AvailableCoinSets model to get the record with the specified set number
               item = AvailableCoinSets.query.get(set_num)
               
               # Check if the item exists and return the transaction count
               if item:
                    return item.tx_count
               else:
                    # Handle the case where the item is not found
                    return 0

          except Exception as e:
               # Log or handle the error appropriately
               flash(f"Error retrieving transaction count: {e} - models.py/get_txn_count")
               return 0
     
     def get_contract_address_count(contract_address):
          count = AvailableCoinSets.query.filter_by(contract_address=contract_address).count()
          return count
     
     def get_contract_address_count_with_status(contract_address,status):
          count = AvailableCoinSets.query.filter_by(contract_address=contract_address,status=status).count()
          return count
               
     def get_all_set_numbers():
          try:
               # Query to get all distinct set_number values
               set_numbers = db.session.query(AvailableCoinSets.set_number).distinct().all()
               # Extract values from tuples
               set_number_list = [set_number[0] for set_number in set_numbers]
               return set_number_list
          except Exception as e:
               print(f"An error occurred: {e}")
               return None
     
     ## to get same active coin avilable sets (same coin different sets)
     @staticmethod
     def get_multiple_coin_sets(status):
        subquery = db.session.query(
            AvailableCoinSets.contract_address,
            func.group_concat(AvailableCoinSets.set_number).label('set_numbers')
        ).filter(
            AvailableCoinSets.status == status
        ).group_by(
            AvailableCoinSets.contract_address
        ).having(
            func.count('*') > 1
        ).subquery()

        results = db.session.query(subquery.c.set_numbers).all()
        return [tuple(row.set_numbers.split(',')) for row in results]

     def check_set_number_exists(set_number):
          exists = db.session.query(db.exists().where(AvailableCoinSets.set_number == set_number)).scalar()
          if exists:
               return True
          else:
               return False
          

     def check_contract_addresses_by_status(overlapping_fee_payers, status):
          result = []
          
          for item in overlapping_fee_payers:
               fee_payer = item.get("fee_payer_address")
               sets = item.get("overlapping_sets")

               # Ensure 'sets' is a list of sets (not a list of lists)
               if not isinstance(sets, tuple):
                    raise ValueError("Expected 'overlapping_sets' to be a list")

               # Flatten the list of sets
               all_sets = sets

               # Filter sets by the given status
               filtered_sets = [set_number for set_number in all_sets
                                   if AvailableCoinSets.query.filter_by(set_number=set_number, status=status).first()]

               # Create a mapping from contract addresses to sets
               contract_map = defaultdict(lambda: {'sets': []})
               for set_number in filtered_sets:
                    contract = AvailableCoinSets.query.filter_by(set_number=set_number, status=status).first()
                    if contract:
                         contract_map[contract.contract_address]['sets'].append(set_number)
               
               # Prepare detailed output for each contract address
               coins = []
               for address, details in contract_map.items():
                    contract_info = AvailableCoinSets.query.filter_by(contract_address=address, status=status).first()
                    coin_sets_count = AvailableCoinSets.get_contract_address_count_with_status(address,2)

                    whale_in_buy_sets =[]
                    whale_in_sell_sets=[]

                    for set in details['sets']:
                         priority= AvailableCoinSets.get_priority(set)
                         if priority=='buy':
                              whale_in_buy_sets.append(set)
                         else:
                              whale_in_sell_sets.append(set)


                    no_of_buy_sets = AvailableCoinSets.get_buy_sets_count(address)
                    no_of_sell_sets = AvailableCoinSets.get_sell_sets_count(address)
                    coins.append({
                         'ticker': contract_info.ticker,
                         'coin_address': address,
                         'amount_of_sets': coin_sets_count,
                         'no_of_buy_sets' : no_of_buy_sets,
                         'no_of_sell_sets': no_of_sell_sets,
                         'whale_in_buy_sets': whale_in_buy_sets,
                         'whale_in_sell_sets': whale_in_sell_sets,
                    })
               
               # Prepare the final result for this fee payer
               if len(coins) >1 :
                    result.append({
                         'whale_address': fee_payer,
                         'total_sets': sorted(filtered_sets),
                         'coins': coins
                    })
               
          return result



          ### SAMPLE OUTPUT ##
          # result: [
          # {
          #      "whale_address": "payer1",
          #      "total_sets": [2, 4, 5, 7, 8],
          #      "coins": [
          #      {
          #           "ticker": "daddy",
          #           "coin_address": "0xabc",
          #           "amount_of_sets": 4,
          #           "whale_buy_sets": [2, , 7 ]
          #           "whale_sell_sets": [ 4,  8]
          #      },
          #      {
          #           "ticker": "TICK5",
          #           "coin_address": "0xghi",
          #           "amount_of_sets": 1,
          #           "whale_buy_sets": [ ]
          #           "whale_in_sets": [5]
          #      }
          #      ]
          # },
          # {
          #      "whale_address": "payer2",
          #      "total_sets": [2, 4, 5, 6, 9],
          #      "coins": [
          #      {
          #           "ticker": "TICK2",
          #           "coin_address": "0xabc",
          #           "amount_of_sets": 3,
          #           "whale_buy_sets": [ 1,2]
          #           "whale_in_sets": [5]
          #      },
          #      {
          #           "ticker": "TICK9",
          #           "coin_address": "0xdef",
          #           "amount_of_sets": 2,
          #           "whale_buy_sets": [1 ]
          #           "whale_in_sets": [4]
          #      }
          #      ]
          # }
          # ]


     @staticmethod
     def get_max_set_number():
        max_set_number = db.session.query(func.max(AvailableCoinSets.set_number)).scalar()
        if max_set_number == None:
          return 0
        return max_set_number
     
     def get_coins_sets_by_status(status):
          transactions = db.session.query(AvailableCoinSets).filter_by(status=status).all()
          return transactions
     
     def get_status_by_set_number(set_number):
          try:
               # Query the database
               result = db.session.query(AvailableCoinSets).filter_by(set_number=set_number).first()
               
               # Check if result is not None
               if result:
                    return result.status
               else:
                    flash("No SET avilable",category='Warning')
                    return None
          except Exception as e:
               print(f"An error occurred: {e}")
               return None
          
     def get_coins_count():
          try:
               # Query to count unique fee_payer addresses within the given set_number
               unique_acounts = db.session.query(
                    db.func.count(db.distinct(AvailableCoinSets.contract_address))
               ).scalar()

               return unique_acounts

          except Exception as e:
               flash(f"Error querying database: {e} - modles.py/get_coins_count()")
               return 0
          
     def get_coins_count_by_status(status):
          try:
               subquery = db.session.query(AvailableCoinSets.contract_address).filter_by(status=status).distinct().subquery()
               unique_accounts = db.session.query(func.count(subquery.c.contract_address)).scalar()

               return unique_accounts

          except Exception as e:
               flash(f"Error querying database: {e} - models.py/get_coins_count_by_status()")
               return 0
          
     def get_sets_count_by_status(status):
          try:
               sets_count = db.session.query(func.count(AvailableCoinSets.set_number)).filter_by(status=status).scalar()
               return sets_count

          except Exception as e:
               flash(f"Error querying database: {e} - models.py/get_sets_count_by_status()")
               return 0
                    
          

     def delete_item(set_num):
          # Step 3: Query the database for the row with the given primary key
          item = AvailableCoinSets.query.get(set_num)
          
          # Step 4: Delete the row if it exists
          if item:
               db.session.delete(item)
               db.session.commit()  # Step 5: Commit the transaction
               return True
          else:
               return False
          
     def update_status(set_num, status_no):
          try:
               # Log the update attempt
               logging.info(f"Updating status for set_number: {set_num} to status_no: {status_no}")

               # Query the database
               stmt = update(AvailableCoinSets).where(AvailableCoinSets.set_number == set_num).values(status=status_no)
               result = db.session.execute(stmt)

               # Commit the transaction
               db.session.commit()

               # Check if any rows were affected
               if result.rowcount > 0:
                    logging.info(f"Update successful for set_number: {set_num}")
                    return True
               else:
                    logging.warning(f"No rows affected for set_number: {set_num}")
                    return False

          except SQLAlchemyError as e:
               logging.error(f"Error updating status for set_number: {set_num} - {e}")
               db.session.rollback()  # Rollback the transaction on error
               return False

          except Exception as e:
               logging.error(f"Unexpected error: {e}")
               db.session.rollback()  # Rollback the transaction on error
               return False
          



     def update_unique_fee_payers_count(set_num, count):
          try:
               # Log the update attempt
               logging.info(f"Updating unique_fee_payers_count for set_number: {set_num} to status_no: {count}")

               # Query the database
               stmt = update(AvailableCoinSets).where(AvailableCoinSets.set_number == set_num).values(uni_wallet_count=count)
               result = db.session.execute(stmt)
               # Commit the transaction
               db.session.commit()
               return True

          except SQLAlchemyError as e:
               logging.error(f"Error updating unique_fee_payers_count for set_number: {set_num} - {e}")
               db.session.rollback()  # Rollback the transaction on error
               return False

          except Exception as e:
               logging.error(f"Unexpected error: {e}")
               db.session.rollback()  # Rollback the transaction on error
               return False
          
     def update_buy_unique_fee_payers_count(set_num, count):
          try:
               # Log the update attempt
               logging.info(f"Updating buy_unique_fee_payers count for set_number: {set_num} to status_no: {count}")

               # Query the database
               stmt = update(AvailableCoinSets).where(AvailableCoinSets.set_number == set_num).values(buy_uni_wallet_count=count)
               result = db.session.execute(stmt)
               # Commit the transaction
               db.session.commit()
               return True

          except SQLAlchemyError as e:
               logging.error(f"Error updating buy_unique_fee_payers count for set_number: {set_num} - {e}")
               db.session.rollback()  # Rollback the transaction on error
               return False

          except Exception as e:
               logging.error(f"Unexpected error: {e}")
               db.session.rollback()  # Rollback the transaction on error
               return False
          
     def update_sell_unique_fee_payers_count(set_num, count):
          try:
               # Log the update attempt
               logging.info(f"Updating sell_unique_fee_payers_count for set_number: {set_num} to status_no: {count}")

               # Query the database
               stmt = update(AvailableCoinSets).where(AvailableCoinSets.set_number == set_num).values(sell_uni_wallet_count=count)
               result = db.session.execute(stmt)
               # Commit the transaction
               db.session.commit()
               return True

          except SQLAlchemyError as e:
               logging.error(f"Error updating sell_unique_fee_payers_count for set_number: {set_num} - {e}")
               db.session.rollback()  # Rollback the transaction on error
               return False

          except Exception as e:
               logging.error(f"Unexpected error: {e}")
               db.session.rollback()  # Rollback the transaction on error
               return False
     
     def update_txn_count(set_num, count):
          try:
               # Log the update attempt
               logging.info(f"Updating txn count  for set_number: {set_num} to status_no: {count}")

               # Query the database
               stmt = update(AvailableCoinSets).where(AvailableCoinSets.set_number == set_num).values(tx_count=count)
               result = db.session.execute(stmt)
               # Commit the transaction
               db.session.commit()
               return True

          except SQLAlchemyError as e:
               logging.error(f"Error updating txn count  for set_number: {set_num} - {e}")
               db.session.rollback()  # Rollback the transaction on error
               return False

          except Exception as e:
               logging.error(f"Unexpected error: {e}")
               db.session.rollback()  # Rollback the transaction on error
               return False
          
     def update_valid_txn_count(set_num, count):
          try:
               # Log the update attempt
               logging.info(f"Updating valid txn count  for set_number: {set_num} to status_no: {count}")

               # Query the database
               stmt = update(AvailableCoinSets).where(AvailableCoinSets.set_number == set_num).values(valid_tx_count=count)
               result = db.session.execute(stmt)
               # Commit the transaction
               db.session.commit()
               return True

          except SQLAlchemyError as e:
               logging.error(f"Error updating valid txn count  for set_number: {set_num} - {e}")
               db.session.rollback()  # Rollback the transaction on error
               return False

          except Exception as e:
               logging.error(f"Unexpected error: {e}")
               db.session.rollback()  # Rollback the transaction on error
               return False
          
     def update_buy_txn_count(set_num, count):
          try:
               # Log the update attempt
               logging.info(f"Updating buy txn count for set_number: {set_num} to status_no: {count}")

               # Query the database
               stmt = update(AvailableCoinSets).where(AvailableCoinSets.set_number == set_num).values(buy_tx_count=count)
               result = db.session.execute(stmt)
               # Commit the transaction
               db.session.commit()
               return True

          except SQLAlchemyError as e:
               logging.error(f"Error updating buy txn count for set_number: {set_num} - {e}")
               db.session.rollback()  # Rollback the transaction on error
               return False

          except Exception as e:
               logging.error(f"Unexpected error: {e}")
               db.session.rollback()  # Rollback the transaction on error
               return False
          
     def update_sell_txn_count(set_num, count):
          try:
               # Log the update attempt
               logging.info(f"Updating sell txn count for set_number: {set_num} to status_no: {count}")

               # Query the database
               stmt = update(AvailableCoinSets).where(AvailableCoinSets.set_number == set_num).values(sell_tx_count=count)
               result = db.session.execute(stmt)
               # Commit the transaction
               db.session.commit()
               return True

          except SQLAlchemyError as e:
               logging.error(f"Error updating sell txn count for set_number: {set_num} - {e}")
               db.session.rollback()  # Rollback the transaction on error
               return False

          except Exception as e:
               logging.error(f"Unexpected error: {e}")
               db.session.rollback()  # Rollback the transaction on error
               return False
          
          
######################################################################################################


## Coin transactions data table

same_signatures=0

class CoinTransactions (db.Model): #coinTransactions
     signature = db.Column(db.String(100),primary_key=True,nullable=False)
     time_stamp = db.Column(db.String(150),nullable=False)
     fee_payer =db.Column(db.String(100),nullable=False)
     bought_token = db.Column(db.String(100),nullable=False)
     bought_token_amount = db.Column(db.Float, nullable=False, default=0.0) 
     sold_token = db.Column(db.String(100),nullable=False)
     sold_token_amount = db.Column(db.Float, nullable=False, default=0.0) 
     status = db.Column(db.String(10),nullable=False) #buy or sell
     sub_category = db.Column(db.String(30),nullable=False,default="unknown") # Partialy buy or sell
     set_number = db.Column(db.Integer, nullable=False)

     # def __init__(self, signature, time_stamp, fee_payer, pre_token_balance, post_token_balance, status, set_number):
     #    self.signature = signature
     #    self.time_stamp = time_stamp
     #    self.fee_payer = fee_payer
     #    self.pre_token_balance = pre_token_balance
     #    self.post_token_balance = post_token_balance
     #    self.status = status
     #    self.set_number = set_number

     def to_dict(self):
        """
        Convert a CoinTransaction object to a dictionary format for JSON serialization.
        
        :return: Dictionary representation of the transaction
        """
        return {
            'signature': self.signature,
            'time_stamp': self.time_stamp,
            'fee_payer': self.fee_payer,
            'bought_token': self.bought_token,
            'bought_token_amount': self.bought_token_amount,
            'sold_token': self.sold_token,
            'sold_token_amount': self.sold_token_amount,
            'status': self.status,
            'sub_category': self.sub_category,
            'set_number': self.set_number
        }

     def get_transactions_by_set_number(set_number):

        """
        This method returns all transactions for a given set_number.
        
        :param set_number: The set number to filter transactions by
        :return: List of CoinTransactions matching the given set_number
        """
        # Query the database for all transactions with the given set_number
        transactions = db.session.query(CoinTransactions).filter_by(set_number=set_number).all()
        return transactions

     @classmethod
     def add_transactions_to_db(cls, transaction_data):
        """
        Add a list of transaction data (CoinTransactions objects) to the database
        in a single transaction. Rolls back if any primary key conflict or other error occurs.
        """
        try:
                     # Merge transactions (upsert) instead of bulk insert
          for transaction in transaction_data:
               db.session.add(transaction)

          db.session.commit()  # Commit the transaction
          message = "Transactions added or updated successfully"
          return True, message
          #   # Bulk insert all transactions at once
          #   db.session.bulk_save_objects(transaction_data)
          #   db.session.commit()  # Commit the transaction
          #   message = "Transactions added successfully"
          #   return True, message

        except IntegrityError as e:
            
            db.session.rollback()  # Rollback in case of primary key conflict or any integrity error
            message = f"Error - Same Signature conflict or other integrity issue: {str(e)}"
            print(str(e))
            return False, message

        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback for any other SQLAlchemy errors
            message = f"Error - Failed to insert transactions into CoinTransactions Table\n reason : {str(e)}"
            print(str(e))
            return False, message

     # Check if a signature already exists
     def check_signature_exists(signature):
          return db.session.query(CoinTransactions).filter_by(signature=signature).first() is not None

     def get_overlapping_fee_payers_from_a_pair(set1, set2):
     # Retrieve priorities for the given sets
          set1_priority = AvailableCoinSets.get_priority(set1)
          set2_priority = AvailableCoinSets.get_priority(set2)
          
          # Check if priorities are different
          if set1_priority == set2_priority:
               return []

          # Query for distinct fee_payers based on set1
          fee_payers_set1 = db.session.query(CoinTransactions.fee_payer).filter(
               CoinTransactions.set_number == set1,
               CoinTransactions.status == set1_priority
          ).distinct().all()

          # Query for distinct fee_payers based on set2
          fee_payers_set2 = db.session.query(CoinTransactions.fee_payer).filter(
               CoinTransactions.set_number == set2,
               CoinTransactions.status == set2_priority
          ).distinct().all()

          # Extract fee_payers from query results
          fee_payers_set1 = {fee_payer[0] for fee_payer in fee_payers_set1}
          fee_payers_set2 = {fee_payer[0] for fee_payer in fee_payers_set2}

          # Find overlapping fee payers
          overlapping_fee_payers = fee_payers_set1.intersection(fee_payers_set2)

          return list(overlapping_fee_payers)
                    

     @staticmethod
     def get_overlapping_fee_payers_of_a_coin(set_group,priority):
          fee_payer_sets = {}

          # Iterate over each set number in the set group
          for set_number in set_group:
               
               set_number = int(set_number)
               set_priority = AvailableCoinSets.get_priority(set_number)
               if set_priority == priority:
               # Query the database for fee payers in the current set number
                    fee_payers = db.session.query(CoinTransactions.fee_payer).filter_by(set_number=set_number,status=priority).distinct().all()
                    fee_payers = {fp.fee_payer for fp in fee_payers}

                    # Add fee payers to the fee_payer_sets dictionary
                    for fee_payer in fee_payers:
                         if fee_payer not in fee_payer_sets:
                              fee_payer_sets[fee_payer] = {set_number}
                         else:
                              fee_payer_sets[fee_payer].add(set_number)

          # Find fee payers that are in more than one set and format the output
          overlapping_fee_payers = [{"fee_payer": fp, "sets": list(sets)} for fp, sets in fee_payer_sets.items() if len(sets) > 1]
          row= AvailableCoinSets.get_item(set_group[0])
          result = {
               "ticker": row.ticker,
               "priority" : priority,
               "no_of_sets":len(set_group),
               "contract_address": row.contract_address,
               "whales_count": len(overlapping_fee_payers),
               "fee_payers": overlapping_fee_payers
          }

          ##### sample out put #####

          #  result = {
          #      "ticker": "daddy",
          #      "priority" : "buy",
          #      "no_of_sets": 4,
          #      "contract_address": "jkajksjsnsjjskjks",
          #      "whales_count": 3,
          #      "fee_payers": [
          #           {"fee_payer": "Big4MGvf4dgmE6YNKegjcGBTkUvvVoi11Qrdw8BGMKen", "sets": [1, 2, 3]},
          #           {"fee_payer": "RPW17KwHtGepfzCuzQsabxGTyPKMUDNwpNuLpBgUM3b", "sets": [1, 2]},
          #           {"fee_payer": "9kDgyDEYGQCShMGMLDS7K9xTtHeWgmfyfYeF4YDTxx5m", "sets": [2, 3]}
          #      ]
          # }
          
          return result
     

     def get_overlapping_fee_payers_of_sets():
          # Step 1: Query the database to get all the unique fee payers and their set numbers
          transactions = db.session.query(CoinTransactions.fee_payer, CoinTransactions.set_number,CoinTransactions.status).distinct().all()
               
          # Step 2: Create a dictionary to store the sets each fee payer is part of
          fee_payer_sets = defaultdict(set)
          for fee_payer, set_number , status in transactions:
               priority = AvailableCoinSets.get_priority(set_number)
               if status == priority:
                    fee_payer_sets[fee_payer].add(set_number)
               
          # Step 3: Identify the fee payers that are overlapping between different set numbers
          overlapping_fee_payers = [
               {"fee_payer_address": fee_payer, "overlapping_sets": tuple(sets)}
               for fee_payer, sets in fee_payer_sets.items() if len(sets) > 1
          ]
          
          return overlapping_fee_payers
          ## out put EXAMPLE

                    # 
                    # "overlapping_fee_payers": [
                    # {
                    #      "fee_payer_address": "payer1",
                    #      "overlapping_sets": [1, 2, 4]
                    # },
                    # {
                    #      "fee_payer_address": "payer2",
                    #      "overlapping_sets": [2, 4]
                    # }
                    # ]
                    # 



     def get_signatures(set_number):
          try:
               # Query the database for the specified set number
               result = db.session.query(CoinTransactions).filter_by(set_number=set_number).all()
               
               # Check if result is not empty
               if result:
                    return result
               else:
                    ##flash("No Coin available", category='warning')
                    return None
          except SQLAlchemyError as e:
               flash(f"An error occurred: {e}", category='error')
               db.session.rollback()  # Rollback the session in case of error
               return None
          except Exception as e:
               flash(f"An unexpected error occurred: {e}", category='error')
               db.session.rollback()  # Rollback the session in case of error
               return None

     def get_last_signature(set_number):
          try:
               # Query to get all signatures for the given set_number, ordered by timestamp or ID in ascending order
               first_signature_record = db.session.query(CoinTransactions).filter_by(set_number=set_number).order_by(CoinTransactions.time_stamp.asc()).first()
               
               if first_signature_record:
                    return first_signature_record.signature
               else:
                    return None
          except SQLAlchemyError as e:
               print(f"An error occurred: {e}")
               return None


     def get_signatures_count(set_number):
          try:
               # Query the database for the count of records with the specified set number
               count = db.session.query(CoinTransactions).filter_by(set_number=set_number).count()
               
               # Return the count
               return count
          except SQLAlchemyError as e:
               # Handle database errors
               flash(f"An error occurred: {e}", category='error')
               db.session.rollback()  # Rollback the session in case of error
               return 0
          except Exception as e:
               # Handle any other unexpected errors
               flash(f"An unexpected error occurred: {e}", category='error')
               db.session.rollback()  # Rollback the session in case of error
               return 0

     def add_new_transaction(txn, set_number,details):
          global same_signatures
          new_txn = CoinTransactions(
               signature=txn['signature'],
               time_stamp=txn['time_stamp'],
               fee_payer=txn['fee_payer'],  # Fee payer
               bought_token = details['bought_token'],
               bought_token_amount = details['bought_token_amount'],
               sold_token = details['sold_token'],
               sold_token_amount = details['sold_token_amount'],
               status = details['status'],
               sub_category = details['sub_category'],
               set_number= set_number # change this
          )
          
          try:
               db.session.add(new_txn)
               db.session.commit()
               same_signatures=0

               return True
          
          except IntegrityError as e:
               db.session.rollback()
               signature = txn['signature']
               item = CoinTransactions.query.get(signature)
               if item is None:
                    flash("Error adding transaction to the database: IntegrityError", "error")
               else:
                    if same_signatures < 50:
                         same_signatures = same_signatures + 1
                         print("SAME SIGNATURE FOUND - "+ str(same_signatures),'info')
                         return True
                    else:
                         flash("ERROR - MORE THAN 50 SAME SIGNATURES ARE FOUND NEARBY(WHEN TRYING TO ADD THE TRANSACTION)", "error")
                         print("ERROR - MORE THAN 50 SAME SIGNATURES ARE FOUND NEARBY(WHEN TRYING TO ADD THE TRANSACTION)", "error")
                         return False
                    
          except SQLAlchemyError as e:
               db.session.rollback()
               flash("Error adding transaction to the database: SQLAlchemyError", "error")
               return False
          except Exception as e:
               db.session.rollback()
               flash("An unexpected error occurred while adding the transaction", "error")
               return False
          
     
     
     def get_buy_txn_count(set_number):
          try:
               # Query the database for the count of records with the specified set number
               count = db.session.query(CoinTransactions).filter_by(set_number=set_number,status="buy").count()
               
               # Return the count
               return count
          except SQLAlchemyError as e:
               # Handle database errors
               flash(f"An error occurred: {e}", category='error')
               db.session.rollback()  # Rollback the session in case of error
               return 0
          except Exception as e:
               # Handle any other unexpected errors
               flash(f"An unexpected error occurred: {e}", category='error')
               db.session.rollback()  # Rollback the session in case of error
               return 0

     def get_sell_txn_count(set_number):
          try:
               # Query the database for the count of records with the specified set number
               count = db.session.query(CoinTransactions).filter_by(set_number=set_number,status="sell").count()
               
               # Return the count
               return count
          except SQLAlchemyError as e:
               # Handle database errors
               flash(f"An error occurred: {e}", category='error')
               db.session.rollback()  # Rollback the session in case of error
               return 0
          except Exception as e:
               # Handle any other unexpected errors
               flash(f"An unexpected error occurred: {e}", category='error')
               db.session.rollback()  # Rollback the session in case of error
               return 0


     def get_unique_fee_payers_count_by_set_number(set_number):
          try:
               # Query to count unique fee_payer addresses within the given set_number
               unique_fee_payers_count = db.session.query(
                    db.func.count(db.distinct(CoinTransactions.fee_payer))
               ).filter(
                    CoinTransactions.set_number == set_number
               ).scalar()

               return unique_fee_payers_count

          except Exception as e:
               flash(f"Error querying database: {e} - modles.py/get_unique_fee_payers_count_by_set_number(set_number)")
               return 0
     def get_sell_or_buy_unique_fee_payers_count_by_set_number(set_number,sell_or_buy):
          try:
               # Query to count unique fee_payer addresses within the given set_number
               unique_fee_payers_count = db.session.query(
                    db.func.count(db.distinct(CoinTransactions.fee_payer))
               ).filter(
                    CoinTransactions.set_number == set_number,
                    CoinTransactions.status == sell_or_buy
               ).scalar()

               return unique_fee_payers_count

          except Exception as e:
               flash(f"Error querying database: {e} - modles.py/get_unique_fee_payers_count_by_set_number(set_number)")
               return 0


     def delete_items(set_num):
          items = CoinTransactions.query.filter_by(set_number=set_num).all()
          
          # Step 4: Delete the rows if they exist
          if items:
               for item in items:
                    db.session.delete(item)
               db.session.commit()  # Step 5: Commit the transaction
               return True
          else:
               return False
          

     def update_transaction_set_number(set_number1, set_number2):
          try:
               # Perform the update operation
               rows_updated = CoinTransactions.query.filter_by(set_number=set_number2).update({'set_number': set_number1})
               
               if rows_updated:
                    db.session.commit()
                    return True
               else:
                    # No rows were updated
                    return False

          except SQLAlchemyError as e:
               # Rollback in case of an error
               db.session.rollback()
               # Optionally log the exception
               print(f"Error updating transaction to the database: {e}")
               # If you are within a Flask route, you can use flash()
               # flash("Error updating transaction to the database: SQLAlchemyError", "error")
               return False
     

###############################################################################################################
class Pairs (db.Model):
     id = db.Column(db.Integer,primary_key=True, nullable=False,autoincrement=True)
     set1 = db.Column(db.Integer,nullable=False)
     set2 = db.Column(db.Integer,nullable=False)
     description =db.Column(db.String(150),nullable=False)

     def add_pair(set1,set2,description):
          try:
               new_entry = Pairs(set1=set1,set2=set2,description=description)
               db.session.add(new_entry)
               db.session.commit()
               return True
          except Exception as e:
               db.session.rollback()
               return False
          
     def get_all_pairs():
          # Query all rows from the Pairs table
          rows = db.session.query(Pairs).all()
          
          # Format the results into a list of tuples with description
          pairs = [(row.set1, row.set2, row.description) for row in rows]
          
          return pairs
     
     def check_pair_existence(num1, num2):
          # Check if the pair (num1, num2) or (num2, num1) exists in the table
          exists = db.session.query(Pairs).filter(
               ((Pairs.set1 == num1) & (Pairs.set2 == num2)) |
               ((Pairs.set1 == num2) & (Pairs.set2 == num1))
          ).first() is not None
          
          return exists
     
     def is_set_number_in_pairs(number):
          # Query to check if the number exists in either set1 or set2
          exists = db.session.query(Pairs).filter(
               (Pairs.set1 == number) | (Pairs.set2 == number)
          ).first() is not None
          
          return exists
     
     def delete_pair(num1, num2):
          # Query to find rows matching the condition
          rows_to_delete = db.session.query(Pairs).filter(
               ((Pairs.set1 == num1) & (Pairs.set2 == num2)) |
               ((Pairs.set1 == num2) & (Pairs.set2 == num1))
          ).all()
          
          if rows_to_delete:
               # Delete the rows
               for row in rows_to_delete:
                    db.session.delete(row)
               db.session.commit()
               return True
          else:
               return False
     
     def delete_pairs_which_include_set_number(number):
          # Query to find rows where the number is in either set1 or set2
          rows_to_delete = db.session.query(Pairs).filter(
               (Pairs.set1 == number) | (Pairs.set2 == number)
          ).all()
          
          if rows_to_delete:
               # Delete the rows
               for row in rows_to_delete:
                    db.session.delete(row)
               db.session.commit()
               return True
          else:
               return False


###############################################################################################################
## API key database
class MoralisApiKey (db.Model):
     id = db.Column(db.Integer,primary_key=True, nullable=False,autoincrement=True)
     api_key = db.Column(db.String(150),nullable=False)

     def add_api(api_key):
          try:
               new_entry = MoralisApiKey(api_key=api_key)
               db.session.add(new_entry)
               db.session.commit()
               return True
          except Exception as e:
               db.session.rollback()
               return False
               
     def get_last_item():
          try:
               last_item = db.session.query(MoralisApiKey).order_by(MoralisApiKey.id.desc()).first()
               return last_item
          except Exception as e:
               print(f"An error occurred: {e}")
               return None
          
     def get_all_items():
          try:
               # Query all items
               items = db.session.query(MoralisApiKey).all()
               
               # Return the list of items
               return items
          except Exception as e:
               print(f"An error occurred: {e}")
               return None

     def delete_Api(api_key):
          # Step 3: Query the database for the row with the given primary key
          item = AvailableCoinSets.query.get(api_key)
          
          # Step 4: Delete the row if it exists
          if item:
               db.session.delete(item)
               db.session.commit()  # Step 5: Commit the transaction
               return True
          else:
               return False


###############################################################################################################
## Gainers

class Gainers(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contractAddress = db.Column(db.String(100), nullable=False)
    walletAddress = db.Column(db.String(100), nullable=False)
    ticker = db.Column(db.String(100), nullable=False)
    gainedProfit = db.Column(db.Float, nullable=False, default=0.0)

    # Add a new Gainer
    @staticmethod
    def add_gainer(contract_address, wallet_address, ticker, gained_profit=0.0):
        try:
            new_gainer = Gainers(
                contractAddress=contract_address,
                walletAddress=wallet_address,
                ticker=ticker,
                gainedProfit=gained_profit
            )
            db.session.add(new_gainer)
            db.session.commit()
            message = "Successfully added the gainer."
            return True, message # Return the new gainer and no error
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback the transaction in case of error
            return False, str(e)  # Return None and the error message

    # Delete a Gainer
    @staticmethod
    def delete_gainer(gainer_id):
        try:
            gainer_to_delete = Gainers.query.get(gainer_id)
            if gainer_to_delete:
                db.session.delete(gainer_to_delete)
                db.session.commit()
                return True, None  # Return True (success) and no error
            return False, "Gainer not found"
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback the transaction in case of error
            return False, str(e)  # Return False and the error message

    # Update a Gainer
    @staticmethod
    def update_gainer(gainer_id, contract_address=None, wallet_address=None, ticker=None, gained_profit=None):
        try:
            gainer_to_update = Gainers.query.get(gainer_id)
            if gainer_to_update:
                if contract_address:
                    gainer_to_update.contractAddress = contract_address
                if wallet_address:
                    gainer_to_update.walletAddress = wallet_address
                if ticker:
                    gainer_to_update.ticker = ticker
                if gained_profit is not None:  # Check for None to differentiate from 0.0
                    gainer_to_update.gainedProfit = gained_profit

                db.session.commit()
                return gainer_to_update, None  # Return the updated gainer and no error
            return None, "Gainer not found"
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback the transaction in case of error
            return None, str(e)  # Return None and the error message

    # Get a Gainer by ID
    @staticmethod
    def get_gainer_by_id(gainer_id):
        try:
            gainer = Gainers.query.get(gainer_id)
            if gainer:
                return gainer, None  # Return the gainer and no error
            return None, "Gainer not found"
        except SQLAlchemyError as e:
            return None, str(e)  # Return None and the error message

    # Get all Gainers
    @staticmethod
    def get_all_gainers():
        try:
            all_gainers = Gainers.query.all()
            return all_gainers, None  # Return all gainers and no error
        except SQLAlchemyError as e:
            return None, str(e)  # Return None and the error message


    # Check if a Gainer with the provided contractAddress and walletAddress exists
    @staticmethod
    def check_existing_gainer(wallet_address, contract_address):
        try:
            # Query to check if a row with the given walletAddress and contractAddress already exists
            existing_gainer = Gainers.query.filter_by(walletAddress=wallet_address, contractAddress=contract_address).first()
           
            if existing_gainer:
                message = "Already exists in the database."
                return True, message  # Return True if a row exists
            message = "Not exists in the database."
            return False,message  # Return False if no matching row is found
        except SQLAlchemyError as e:
            return False,str(e) 
     

     # Get all Gainers with the same walletAddress
    @staticmethod
    def get_gainers_by_wallet_address(wallet_address):
        try:
            # Query to get all rows with the same walletAddress
            gainers = Gainers.query.filter_by(walletAddress=wallet_address).all()
            if gainers:
                return gainers  # Return the list of gainers and no error
            return None, "No gainers found with the provided wallet address."
        except SQLAlchemyError as e:
            return None, str(e)
        
#     @staticmethod
#     def get_gainers_with_duplicate_wallets():
#         try:
#             # Find walletAddresses that appear more than once in the database
#             duplicates = db.session.query(
#                 Gainers.walletAddress, 
#                 func.count(Gainers.walletAddress).label('count')
#             ).group_by(Gainers.walletAddress).having(func.count(Gainers.walletAddress) > 1).all()

#             # If there are duplicates, get all the gainers with those wallet addresses
#             if duplicates:
#                 result = []
#                 # Iterate through each duplicate wallet address
#                 for duplicate in duplicates:
#                     wallet_address = duplicate.walletAddress
#                     count = duplicate.count

#                     # Get all rows for the current wallet address
#                     gainers_data = Gainers.query.filter_by(walletAddress=wallet_address).all()
#                     gainer_data_list = [
#                         {
#                             "id": gainer.id,
#                             "contractAddress": gainer.contractAddress,
#                             "walletAddress": gainer.walletAddress,
#                             "ticker": gainer.ticker,
#                             "gainedProfit": gainer.gainedProfit
#                         }
#                         for gainer in gainers_data
#                     ]

#                     result.append({
#                         "walletAddress": wallet_address,
#                         "count": count,
#                         "data": gainer_data_list
#                     })

#                 # Sort the result by count in descending order
#                 result.sort(key=lambda x: x['count'], reverse=True)

#                 return result, None  # Return the formatted result
#             return None, "No duplicate wallet addresses found."
        
#         except SQLAlchemyError as e:
#             return None, str(e)

    @staticmethod
    def get_gainers_with_duplicate_wallets():
        try:
            # Find walletAddresses that appear more than once in the database
            duplicates = db.session.query(
                Gainers.walletAddress, 
                func.count(Gainers.walletAddress).label('count'),
                func.sum(Gainers.gainedProfit).label('totalProfit')  # Calculate total profit for each wallet address
            ).group_by(Gainers.walletAddress).having(func.count(Gainers.walletAddress) > 1).all()

            # If there are duplicates, get all the gainers with those wallet addresses
            if duplicates:
                result = []
                # Iterate through each duplicate wallet address
                for duplicate in duplicates:
                    wallet_address = duplicate.walletAddress
                    count = duplicate.count
                    total_profit = duplicate.totalProfit  # Get the total profit for this wallet address

                    # Get all rows for the current wallet address
                    gainers_data = Gainers.query.filter_by(walletAddress=wallet_address).all()
                    gainer_data_list = [
                        {
                            "id": gainer.id,
                            "contractAddress": gainer.contractAddress,
                            "walletAddress": gainer.walletAddress,
                            "ticker": gainer.ticker,
                            "gainedProfit": gainer.gainedProfit
                        }
                        for gainer in gainers_data
                    ]

                    result.append({
                        "walletAddress": wallet_address,
                        "count": count,
                        "totalProfit": total_profit,  # Include total profit in the result
                        "data": gainer_data_list
                    })

                # Sort the result by count in descending order
                result.sort(key=lambda x: x['count'], reverse=True)

                return result, None  # Return the formatted result
            return None, "No duplicate wallet addresses found."
        
        except SQLAlchemyError as e:
            return None, str(e)


class BackupFolder(db.Model):
     id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary Key
     ticker = db.Column(db.String(100), nullable=False)  # Ticker
     set_number = db.Column(db.Integer, default =0)
     contract_address = db.Column(db.String(100), nullable=False)  # Contract Address
     searched_from_date_time = db.Column(db.String(100), nullable=False)  # From Date Time
     searched_to_date_time = db.Column(db.String(100), nullable=False)  # To Date Time
     from_signature = db.Column(db.String(255), nullable=True)  # From Signature
     to_signature = db.Column(db.String(255), nullable=True)  # To Signature
     from_block_timestamp = db.Column(db.String(100), nullable=True)  # From Block Timestamp
     to_block_timestamp = db.Column(db.String(100), nullable=True)  # To Block Timestamp
     low_value = db.Column(db.Float, nullable=False)  # Low Value
     peak_value = db.Column(db.Float, nullable=False)  # Peak Value
     description = db.Column(db.String(255), nullable=True)  # Description
     priority = db.Column(db.String(10),nullable=False,default="no")
     txns =db.Column(db.Integer)
     file_name = db.Column(db.String(255), nullable=True)  # File Name
     status = db.Column(db.Integer) # 0-partialy running ,1 - pending_folder , 2-added_folder , -1 - delete_folder

     def to_dict(self):
        return {
            'id': self.id,
            'ticker': self.ticker,
            'set_number': self.set_number,
            'contract_address': self.contract_address,
            'searched_from_date_time': self.searched_from_date_time,
            'searched_to_date_time': self.searched_to_date_time,
            'from_signature': self.from_signature,
            'to_signature': self.to_signature,
            'from_block_timestamp': self.from_block_timestamp,
            'to_block_timestamp': self.to_block_timestamp,
            'low_value': self.low_value,
            'peak_value': self.peak_value,
            'description': self.description,
            'priority': self.priority,
            'txns': self.txns,
            'file_name': self.file_name,
            'status': self.status
        }
     def __repr__(self):
        return f'<BackUpFolder {self.id} - {self.ticker}>'
    

     @staticmethod
     def add_record(ticker,set_number, contract_address, searched_from_date_time, searched_to_date_time, 
                   from_signature, to_signature, from_block_timestamp, to_block_timestamp, 
                   low_value, peak_value, description, priority,txns, file_name, status):
        
       
        try:
            # Create a new record instance
            new_record = BackupFolder(
                ticker=ticker,
                set_number=set_number,
                contract_address=contract_address,
                searched_from_date_time=searched_from_date_time,
                searched_to_date_time=searched_to_date_time,
                from_signature=from_signature,
                to_signature=to_signature,
                from_block_timestamp=from_block_timestamp,
                to_block_timestamp=to_block_timestamp,
                low_value=low_value,
                peak_value=peak_value,
                description=description,
                priority=priority,
                txns = txns,
                file_name=file_name,
                status=status
            )
            
            # Add the new record to the session and commit
            db.session.add(new_record)
            db.session.commit()
            return True, None  # Returning the new record and no error message
        
        except Exception as e:
               print(e)
               db.session.rollback()  # Rollback in case of error
               return False, str(e)  # Return None and the error message

     @staticmethod
     def update_record(record_id, **updates):
          try:
               # Find the record by id
               record = BackupFolder.query.get(record_id)
               if not record:
                    return None, "Record not found"

               # Update fields from the passed updates dictionary
               for key, value in updates.items():
                    if hasattr(record, key):
                         setattr(record, key, value)

               # Commit the changes to the database
               db.session.commit()
               return record, None  # Returning the updated record and no error message
          
          except Exception as e:
               db.session.rollback()  # Rollback in case of error
               return None, str(e)  # Return None and the error message


     @staticmethod
     def delete_record(record_id):
          try:
               # Find the record by id
               record = BackupFolder.query.get(record_id)
               if not record:
                    return None, "Record not found"
               
               # Delete the record from the session
               db.session.delete(record)
               db.session.commit()
               return None, None  # Return None if deletion is successful
          
          except Exception as e:
               db.session.rollback()  # Rollback in case of error
               return None, str(e)  # Return the error message
        
     @staticmethod
     def get_all_sets_in_pending_folder():
          try:
               # Query to get all records where status equals 0 (pending folder)
               pending_folders = BackupFolder.query.filter_by(status=1).order_by(BackupFolder.id.desc()).all()
               data_list = [folder.to_dict() for folder in pending_folders]
               if pending_folders:
                    return True, data_list, None  # Return the list of records
               return True,[], "No pending files found."  # Return empty list if no records found

          except Exception as e:
               return False,[], str(e)  # Return empty list and error message if something goes wrong


     # Update status of a record based on the provided id
     def update_status_by_id(folder_id, new_status):
          try:
               # Fetch the record by ID
               folder = BackupFolder.query.get(folder_id)

               if not folder:
                    message= "This row Id data not found in data base"
                    return False, message

               # Update the status
               folder.status = new_status
               db.session.commit()  # Commit the change to the database
               message = "Succesfully Remove from Pending Folder"
               return True,message

          except Exception as e:
               message = "Database Exception error occured at update_status_by_id () method"
               return False,message
          
     # Update status of a record based on the provided id
     def update_set_number_by_id(folder_id, set_number):
          try:
               # Fetch the record by ID
               folder = BackupFolder.query.get(folder_id)

               if not folder:
                    message= "This row Id data not found in data base"
                    return False, message

               # Update the status
               folder.set_number = set_number
               db.session.commit()  # Commit the change to the database
               message = "Succesfully Update set number"
               return True,message

          except Exception as e:
               message = "Database Exception error occured at update_status_by_id () method"
               return False,message
          
          

     # Get file path by the provided ID
     def get_file_path_by_id(folder_id):
          try:
               # Fetch the record by ID
               folder = BackupFolder.query.get(folder_id)

               if not folder:
                    message = "error: Folder not found"
                    return False , message

               # Return the file name (file path)
               return True, folder.file_name

          except Exception as e:
               message = "Database Exception error occured at get_file_path_by_id () method"
               return False , message
          
          
     def get_row_id_from_set_number(set_number):
          try:
               # Fetch the record by set_number
               row = BackupFolder.query.filter_by(set_number=set_number).first()

               if not row:
                    message = "error: row not found"
                    return False, message

               # Return the row ID
               return True, row

          except Exception as e:
               message = f"Database exception error occurred: {str(e)}"
               return False, message


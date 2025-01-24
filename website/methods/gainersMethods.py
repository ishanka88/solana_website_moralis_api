from website.modles import Gainers
from website import db
from flask import flash
from sqlalchemy.exc import SQLAlchemyError

def addGainers(contractAddress, walletAddress, ticker, gained_profit):
    try:

        check =Gainers.check_existing_gainer(walletAddress, contractAddress)
        # Check if the gainer with the same walletAddress and contractAddress exists
        if check[0]:
            return False, check[1]  # Return False if the gainer exists
        
        # Add new gainer if not exists
        status = Gainers.add_gainer(contractAddress, walletAddress, ticker, gained_profit)
        return status  # Return True if the gainer was successfully added
    
    except SQLAlchemyError as e:
        # Catch any database-related errors
        message = f"Database error - {str(e)}"
        return False, message  # Return False with a specific error message
    
    except Exception as e:
        # Catch any other errors that occur during the process
        message = f"An error occurred: {str(e)}"
        return False, message  # Return False with a specific error message

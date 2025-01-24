from website.modles import AvailableCoinSets,CoinTransactions
from website import db
from flask import flash

def getFromCoins(status):
    same_coin_sets =AvailableCoinSets.get_multiple_coin_sets(status)
    # print(same_coin_sets)

    if (same_coin_sets):
        whales_sets_set=[]
        for set_group in same_coin_sets:
            couple=[]
            whales_set = CoinTransactions.get_overlapping_fee_payers_of_a_coin(set_group,"buy")
            if whales_set :
                couple.append(whales_set)
            else:
                couple.append(False)

            whales_set = CoinTransactions.get_overlapping_fee_payers_of_a_coin(set_group,"sell")
            if whales_set :
                couple.append(whales_set)
            else:
                couple.append(False)
            if couple[0]!=False or couple[1]!=False:
                data= buy_and_sell_whales_in_a_single_data(couple)
                whales_sets_set.append(data)
        return whales_sets_set
                    
    return []

    
def buy_and_sell_whales_in_a_single_data (couple):
               
        
        if couple[0]!=False and couple[1]!=False :
            data =couple[0]
            buy_whales_count=couple[0]["whales_count"]
            sell_whales_count=couple[1]["whales_count"]

            buy_fee_payers = couple[0]["fee_payers"]
            sell_fee_payers = couple[1]["fee_payers"]

            overlapping_payers =[]

            fee_payers = []


            for sell_fee_payer in sell_fee_payers:
                x=0
                for buy_fee_payer in buy_fee_payers:
                    if sell_fee_payer["fee_payer"] == buy_fee_payer["fee_payer"] :
                        x=1
                        overlapping_payers.append(sell_fee_payer["fee_payer"] )

                        fee_payer = {"fee_payer": sell_fee_payer["fee_payer"] , "sets":[buy_fee_payer["sets"],sell_fee_payer["sets"]]}
                        fee_payers.append(fee_payer)
                        break
                if x==0:
                    fee_payer = {"fee_payer": sell_fee_payer["fee_payer"], "sets":[False,sell_fee_payer["sets"]]}
                    fee_payers.append(fee_payer)
                    
            for buy_fee_payer in buy_fee_payers:
                x=0
                for overlapping_payer in overlapping_payers:
                    if buy_fee_payer["fee_payer"] == overlapping_payer:
                        x=1
                        break
                        
                if x==0:

                    fee_payer = {"fee_payer": buy_fee_payer["fee_payer"], "sets":[buy_fee_payer["sets"],False]}
                    fee_payers.append(fee_payer)
            no_of_buy_sets = AvailableCoinSets.get_buy_sets_count(data["contract_address"])
            no_of_sell_sets = AvailableCoinSets.get_sell_sets_count(data["contract_address"])
               
  
            result = {
               "ticker": data ["ticker"],
               "no_of_sets": data["no_of_sets"],
               "no_of_buy_sets": no_of_buy_sets,
               "no_of_sell_sets": no_of_sell_sets,
               "contract_address": data["contract_address"],
               "buy_whales_count": buy_whales_count,
               "sell_whales_count": sell_whales_count,
               "fee_payers":fee_payers,
            }

        else:

            if couple[0]!=False:
                data = couple[0]
                buy_whales_count=couple[0]["whales_count"]
                sell_whales_count = 0

                fee_payers=[]

                for buy_fee_payer in couple[0]["fee_payers"]:
                    fee_payer = {"fee_payer": buy_fee_payer["fee_payer"], "sets":[buy_fee_payer["sets"],False]}
                    fee_payers.append(fee_payer)
            else:
                data = couple[1]
                sell_whales_count=couple[1]["whales_count"]
                buy_whales_count = 0

                fee_payers=[]

                for sell_fee_payer in couple[1]["fee_payers"]:
                    fee_payer = {"fee_payer": sell_fee_payer["fee_payer"], "sets":[False,sell_fee_payer["sets"]]}
                    fee_payers.append(fee_payer)

            no_of_buy_sets = AvailableCoinSets.get_buy_sets_count(data["contract_address"])
            no_of_sell_sets = AvailableCoinSets.get_sell_sets_count(data["contract_address"])
               
            
            result = {
               "ticker": data ["ticker"],
               "no_of_sets": data["no_of_sets"],
               "no_of_buy_sets": no_of_buy_sets,
               "no_of_sell_sets": no_of_sell_sets,
               "contract_address": data["contract_address"],
               "buy_whales_count": buy_whales_count,
               "sell_whales_count": sell_whales_count,
               "fee_payers":fee_payers,
            }

        ### SAMPLE OUTPUT ### 
          #  result = {
          #      "ticker": "daddy",
          #      "no_of_sets": 4,
          #      "contract_address": "jkajksjsnsjjskjks",
          #      "buy_whales_count": 3,
          #      "sell_whales_count": 3,
          #          'fee_payers': [
          #                 {'fee_payer': '8v8NmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP', 'sets': [[1, 2, 3], False]}, 
          #                 {'fee_payer': '16vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP', 'sets': [False, [1, 2]]}, 
          #                 {'fee_payer': '9v8NmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP', 'sets': [[1, 2], False]}, 
          #                 {'fee_payer': '10vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP', 'sets': [[2, 3], False]}
          #                 ]
        #   # }       
        # }
        return result




def getFromAllSets(status):
 
    if status is None:
        flash("Error- status should be added")
        return 
    
    overlapping_fee_payers = CoinTransactions.get_overlapping_fee_payers_of_sets()
    result = AvailableCoinSets.check_contract_addresses_by_status(overlapping_fee_payers, status)
    
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
          #           "whale_in_buy_sets": [2, , 7 ]
          #           "whale_in_sell_sets": [ 4,  8]
          #      },
          #      {
          #           "ticker": "TICK5",
          #           "coin_address": "0xghi",
          #           "amount_of_sets": 1,
          #           "whale_in_buy_sets": [ ]
          #           "whale_in_sell_sets": [5]
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


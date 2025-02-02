from website.modles import AvailableCoinSets,CoinTransactions,Pairs


def get_available_pairs ():

    result =[]
    available_pairs_sets =Pairs.get_all_pairs()

    for set in available_pairs_sets:
        set1=set[0]
        set2=set[1]
        description=set[2]
        priority = AvailableCoinSets.get_priority(set1)
        
        if priority == 'buy':
            buy_set_no=set1
            sell_set_no=set2
        else:
            buy_set_no=set2
            sell_set_no=set1

        coin = AvailableCoinSets.get_item(set1)
        contract_address= coin.contract_address
        ticker= coin.ticker
        
        pair = {
            'ticker': ticker,
            'contract_address':contract_address,
            'buy_set_no': buy_set_no,
            'sell_set_no': sell_set_no,
            'description': description,
        }
        result.append(pair)
        
    return result



def get_whales_from_pairs (data):
    whales_data=[]
    for pair in data:
       buy_set_no= pair["buy_set_no"]
       sell_set_no= pair["sell_set_no"]
       whales=CoinTransactions.get_overlapping_fee_payers_from_a_pair(buy_set_no,sell_set_no)
       if whales:
           whales_set=[]
           for whale in whales:
               item = {
                   "whale_adress":whale
               }
               whales_set.append(item)
           whales_pair = {      
                'contract_asdress': pair["contract_address"],
                'ticker': pair["ticker"],
                'buy_set_no': pair["buy_set_no"],
                'sell_set_no': pair["sell_set_no"],
                'whales': whales_set
                }
           whales_data.append(whales_pair)

    return whales_data

#### Sample data##
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

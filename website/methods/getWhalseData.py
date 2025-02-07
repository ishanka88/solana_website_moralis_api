from website.modles import AvailableCoinSets
from website.methods import whalesCa
from config import Config



def getWhales():
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

    whale_table_data = whalesCa.getFromAllSets(2)

    Config.WHALE_PAGE_MAIN_TABLE_DATA ={'whales': whale_table_data , 'status_data':status_data} 


    # ## ADD SAMPLE DATA TO DATABASE
    # isha = AvailableCoinSets.get_coins_count()
    # if isha == 0 :
                
    #         dataValue = [         
    #             [
    #                 1, "4Cnk9EPnW5ixfLZatCPJjDB1PUtcRpVVgTQukm9epump", "daddy","abc","buy",1722150406, 1722159978, 
    #                 "fjLoquM447odNVwr8wx3uuwcGCJA6z7JWRkc9aVdJ2xXM7H4s6M7guzVg14QCQtwHEiNgbjzxqTt75SQrHMBfhK", 
    #                 "2XQhcKzvKP6Bu6mjfjN8zmdB42ZhdHYgPvh5R6Fi1GvuphDgfEtKQakDrrFGAh4S8PkpKvWPiL1kVpc9ekgHmZA5", 
    #                 "248jjeZgtdsxL2Za3mA6GX1NVkshjcjCtCZFKBu7V1MWPU539jaS5UP6tSxjekeJWvP7ppPD73VtcEpwtixn2xKX", 
    #                 377, 216, 10,15,30,12,12,1,2,0,2
    #             ],
    #             [
    #                 2, "4Cnk9EPnW5ixfLZatCPJjDB1PUtcRpVVgTQukm9epump", "daddy","abc","buy",1722150407, 1722159979, 
    #                 "fjLoquM447odNVwr8wx3uuwcGCJA6z7JWRkc9aVdJ2xXM7H4s6M7guzVg14QCQtwHEiNgbjzxqTt75SQrHMBfhK", 
    #                 "2XQhcKzvKP6Bu6mjfjN8zmdB42ZhdHYgPvh5R6Fi1GvuphDgfEtKQakDrrFGAh4S8PkpKvWPiL1kVpc9ekgHmZA5", 
    #                 "248jjeZgtdsxL2Za3mA6GX1NVkshjcjCtCZFKBu7V1MWPU539jaS5UP6tSxjekeJWvP7ppPD73VtcEpwtixn2xKX", 
    #                 377, 216, 10,15,30,12,12,1,2,0,2
    #             ],
    #             [
    #                 3, "4Cnk9EPnW5ixfLZatCPJjDB1PUtcRpVVgTQukm9epump", "daddy","abc","buy",1722150407, 1722159979, 
    #                 "fjLoquM447odNVwr8wx3uuwcGCJA6z7JWRkc9aVdJ2xXM7H4s6M7guzVg14QCQtwHEiNgbjzxqTt75SQrHMBfhK", 
    #                 "2XQhcKzvKP6Bu6mjfjN8zmdB42ZhdHYgPvh5R6Fi1GvuphDgfEtKQakDrrFGAh4S8PkpKvWPiL1kVpc9ekgHmZA5", 
    #                 "248jjeZgtdsxL2Za3mA6GX1NVkshjcjCtCZFKBu7V1MWPU539jaS5UP6tSxjekeJWvP7ppPD73VtcEpwtixn2xKX", 
    #                 377, 216, 10,15,30,12,12,1,2,0,2
    #             ],
    #             [
    #                 4, "4Cnk9EPnW5ixfLZatCPJjDB1PUtcRpVVgTQukm9epump", "daddy","abc","sell",1722150407, 1722159979, 
    #                 "fjLoquM447odNVwr8wx3uuwcGCJA6z7JWRkc9aVdJ2xXM7H4s6M7guzVg14QCQtwHEiNgbjzxqTt75SQrHMBfhK", 
    #                 "2XQhcKzvKP6Bu6mjfjN8zmdB42ZhdHYgPvh5R6Fi1GvuphDgfEtKQakDrrFGAh4S8PkpKvWPiL1kVpc9ekgHmZA5", 
    #                 "248jjeZgtdsxL2Za3mA6GX1NVkshjcjCtCZFKBu7V1MWPU539jaS5UP6tSxjekeJWvP7ppPD73VtcEpwtixn2xKX", 
    #                 377, 216, 10,15,30,12,12,1,2,0,2
    #             ],
    #             [
    #                 5, "4Cnk9EPnW5ixfLZatCPJjDB1PUtcRpVVgTQukm9epump", "daddy","abc","sell",1722150407, 1722159979, 
    #                 "fjLoquM447odNVwr8wx3uuwcGCJA6z7JWRkc9aVdJ2xXM7H4s6M7guzVg14QCQtwHEiNgbjzxqTt75SQrHMBfhK", 
    #                 "2XQhcKzvKP6Bu6mjfjN8zmdB42ZhdHYgPvh5R6Fi1GvuphDgfEtKQakDrrFGAh4S8PkpKvWPiL1kVpc9ekgHmZA5", 
    #                 "248jjeZgtdsxL2Za3mA6GX1NVkshjcjCtCZFKBu7V1MWPU539jaS5UP6tSxjekeJWvP7ppPD73VtcEpwtixn2xKX", 
    #                 377, 216, 10,15,30,12,12,1,2,0,2
    #             ],
    #             [
    #                  6, "4Cnk9EPnW5ixfLZatCPJjDB1PUtcRpVVgTQukm9epump", "daddy","abc","sell",1722150407, 1722159979, 
    #                 "fjLoquM447odNVwr8wx3uuwcGCJA6z7JWRkc9aVdJ2xXM7H4s6M7guzVg14QCQtwHEiNgbjzxqTt75SQrHMBfhK", 
    #                 "2XQhcKzvKP6Bu6mjfjN8zmdB42ZhdHYgPvh5R6Fi1GvuphDgfEtKQakDrrFGAh4S8PkpKvWPiL1kVpc9ekgHmZA5", 
    #                 "248jjeZgtdsxL2Za3mA6GX1NVkshjcjCtCZFKBu7V1MWPU539jaS5UP6tSxjekeJWvP7ppPD73VtcEpwtixn2xKX", 
    #                 377, 216, 10,15,30,12,12,1,2,0,2
    #             ],
    #             [
    #                  7, "4Cnk9EPnW5ixfLZatCPJjDB1PUtcRpVVgTQukm9epump", "daddy","abc","sell",1722150407, 1722159979, 
    #                 "fjLoquM447odNVwr8wx3uuwcGCJA6z7JWRkc9aVdJ2xXM7H4s6M7guzVg14QCQtwHEiNgbjzxqTt75SQrHMBfhK", 
    #                 "2XQhcKzvKP6Bu6mjfjN8zmdB42ZhdHYgPvh5R6Fi1GvuphDgfEtKQakDrrFGAh4S8PkpKvWPiL1kVpc9ekgHmZA5", 
    #                 "248jjeZgtdsxL2Za3mA6GX1NVkshjcjCtCZFKBu7V1MWPU539jaS5UP6tSxjekeJWvP7ppPD73VtcEpwtixn2xKX", 
    #                 377, 216, 10,15,30,12,12,1,2,0,2
    #             ],


	# 	        [
    #                  8, "3B5wuUrMEi5yATD7on46hKfej3pfmd7t1RKgrsN3pump", "billy","abc","buy",1722150407, 1722159979, 
    #                 "fjLoquM447odNVwr8wx3uuwcGCJA6z7JWRkc9aVdJ2xXM7H4s6M7guzVg14QCQtwHEiNgbjzxqTt75SQrHMBfhK", 
    #                 "2XQhcKzvKP6Bu6mjfjN8zmdB42ZhdHYgPvh5R6Fi1GvuphDgfEtKQakDrrFGAh4S8PkpKvWPiL1kVpc9ekgHmZA5", 
    #                 "248jjeZgtdsxL2Za3mA6GX1NVkshjcjCtCZFKBu7V1MWPU539jaS5UP6tSxjekeJWvP7ppPD73VtcEpwtixn2xKX", 
    #                 377, 216, 10,15,30,12,12,1,2,0,2
    #             ],
    #             [
    #                  9, "3B5wuUrMEi5yATD7on46hKfej3pfmd7t1RKgrsN3pump", "billy","abc","buy",1722150407, 1722159979, 
    #                 "fjLoquM447odNVwr8wx3uuwcGCJA6z7JWRkc9aVdJ2xXM7H4s6M7guzVg14QCQtwHEiNgbjzxqTt75SQrHMBfhK", 
    #                 "2XQhcKzvKP6Bu6mjfjN8zmdB42ZhdHYgPvh5R6Fi1GvuphDgfEtKQakDrrFGAh4S8PkpKvWPiL1kVpc9ekgHmZA5", 
    #                 "248jjeZgtdsxL2Za3mA6GX1NVkshjcjCtCZFKBu7V1MWPU539jaS5UP6tSxjekeJWvP7ppPD73VtcEpwtixn2xKX", 
    #                 377, 216, 10,15,30,12,12,1,2,0,2
    #             ],
	# 	        [
    #                  10, "3B5wuUrMEi5yATD7on46hKfej3pfmd7t1RKgrsN3pump", "billy","abc","sell",1722150407, 1722159979, 
    #                 "fjLoquM447odNVwr8wx3uuwcGCJA6z7JWRkc9aVdJ2xXM7H4s6M7guzVg14QCQtwHEiNgbjzxqTt75SQrHMBfhK", 
    #                 "2XQhcKzvKP6Bu6mjfjN8zmdB42ZhdHYgPvh5R6Fi1GvuphDgfEtKQakDrrFGAh4S8PkpKvWPiL1kVpc9ekgHmZA5", 
    #                 "248jjeZgtdsxL2Za3mA6GX1NVkshjcjCtCZFKBu7V1MWPU539jaS5UP6tSxjekeJWvP7ppPD73VtcEpwtixn2xKX", 
    #                 377, 216, 10,15,30,12,12,1,2,0,2
    #             ],
    #             [
    #                  11, "3B5wuUrMEi5yATD7on46hKfej3pfmd7t1RKgrsN3pump", "billy","abc","sell",1722150407, 1722159979, 
    #                 "fjLoquM447odNVwr8wx3uuwcGCJA6z7JWRkc9aVdJ2xXM7H4s6M7guzVg14QCQtwHEiNgbjzxqTt75SQrHMBfhK", 
    #                 "2XQhcKzvKP6Bu6mjfjN8zmdB42ZhdHYgPvh5R6Fi1GvuphDgfEtKQakDrrFGAh4S8PkpKvWPiL1kVpc9ekgHmZA5", 
    #                 "248jjeZgtdsxL2Za3mA6GX1NVkshjcjCtCZFKBu7V1MWPU539jaS5UP6tSxjekeJWvP7ppPD73VtcEpwtixn2xKX", 
    #                 377, 216, 10,15,30,12,12,1,2,0,2
    #             ],
    #              [
    #                  12, "0x9e22B4f836a461ddC7765E5fAd693688e76E6069", "chad","abc","buy",1722150407, 1722159979, 
    #                 "fjLoquM447odNVwr8wx3uuwcGCJA6z7JWRkc9aVdJ2xXM7H4s6M7guzVg14QCQtwHEiNgbjzxqTt75SQrHMBfhK", 
    #                 "2XQhcKzvKP6Bu6mjfjN8zmdB42ZhdHYgPvh5R6Fi1GvuphDgfEtKQakDrrFGAh4S8PkpKvWPiL1kVpc9ekgHmZA5", 
    #                 "248jjeZgtdsxL2Za3mA6GX1NVkshjcjCtCZFKBu7V1MWPU539jaS5UP6tSxjekeJWvP7ppPD73VtcEpwtixn2xKX", 
    #                 377, 216, 10,15,30,12,12,1,2,0,2
    #             ],
    #              [
    #                  13, "0x9e22B4f836a461ddC7765E5fAd693688e76E6069", "chad","abc","buy",1722150407, 1722159979, 
    #                 "fjLoquM447odNVwr8wx3uuwcGCJA6z7JWRkc9aVdJ2xXM7H4s6M7guzVg14QCQtwHEiNgbjzxqTt75SQrHMBfhK", 
    #                 "2XQhcKzvKP6Bu6mjfjN8zmdB42ZhdHYgPvh5R6Fi1GvuphDgfEtKQakDrrFGAh4S8PkpKvWPiL1kVpc9ekgHmZA5", 
    #                 "248jjeZgtdsxL2Za3mA6GX1NVkshjcjCtCZFKBu7V1MWPU539jaS5UP6tSxjekeJWvP7ppPD73VtcEpwtixn2xKX", 
    #                 377, 216, 10,15,30,12,12,1,2,0,2
    #             ],
    #              [
    #                  14, "0x9e22B4f836a461ddC7765E5fAd693688e76E6069", "chad","abc","buy",1722150407, 1722159979, 
    #                 "fjLoquM447odNVwr8wx3uuwcGCJA6z7JWRkc9aVdJ2xXM7H4s6M7guzVg14QCQtwHEiNgbjzxqTt75SQrHMBfhK", 
    #                 "2XQhcKzvKP6Bu6mjfjN8zmdB42ZhdHYgPvh5R6Fi1GvuphDgfEtKQakDrrFGAh4S8PkpKvWPiL1kVpc9ekgHmZA5", 
    #                 "248jjeZgtdsxL2Za3mA6GX1NVkshjcjCtCZFKBu7V1MWPU539jaS5UP6tSxjekeJWvP7ppPD73VtcEpwtixn2xKX", 
    #                 377, 216, 10,15,30,12,12,1,2,0,2
    #             ],
    #              [
    #                  15, "0x9e22B4f836a461ddC7765E5fAd693688e76E6069", "chad","abc","sell",1722150407, 1722159979, 
    #                 "fjLoquM447odNVwr8wx3uuwcGCJA6z7JWRkc9aVdJ2xXM7H4s6M7guzVg14QCQtwHEiNgbjzxqTt75SQrHMBfhK", 
    #                 "2XQhcKzvKP6Bu6mjfjN8zmdB42ZhdHYgPvh5R6Fi1GvuphDgfEtKQakDrrFGAh4S8PkpKvWPiL1kVpc9ekgHmZA5", 
    #                 "248jjeZgtdsxL2Za3mA6GX1NVkshjcjCtCZFKBu7V1MWPU539jaS5UP6tSxjekeJWvP7ppPD73VtcEpwtixn2xKX", 
    #                 377, 216, 10,15,30,12,12,1,2,0,2
    #             ],
    #              [
    #                  16, "0x9e22B4f836a461ddC7765E5fAd693688e76E6069", "chad","abc","sell",1722150407, 1722159979, 
    #                 "fjLoquM447odNVwr8wx3uuwcGCJA6z7JWRkc9aVdJ2xXM7H4s6M7guzVg14QCQtwHEiNgbjzxqTt75SQrHMBfhK", 
    #                 "2XQhcKzvKP6Bu6mjfjN8zmdB42ZhdHYgPvh5R6Fi1GvuphDgfEtKQakDrrFGAh4S8PkpKvWPiL1kVpc9ekgHmZA5", 
    #                 "248jjeZgtdsxL2Za3mA6GX1NVkshjcjCtCZFKBu7V1MWPU539jaS5UP6tSxjekeJWvP7ppPD73VtcEpwtixn2xKX", 
    #                 377, 216, 10,15,30,12,12,1,2,0,2
    #             ]


    #        ]              


    #         for x in dataValue:
    #             AvailableCoinSets.add_new_set(x)


    #         data23 = [

    #             ## buy
                
                
    #                 {"signature": "256541654","time_stamp":123, "fee_payer": "8v8NmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 1},
    #                 {"signature": "256541655","time_stamp":123, "fee_payer": "8v8NmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":13, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 2},
    #                 {"signature": "256541656","time_stamp":123, "fee_payer": "8v8NmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":14, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 3},


    #                 {"signature": "256541657","time_stamp":123, "fee_payer": "9v8NmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 1},
    #                 {"signature": "256541658","time_stamp":123, "fee_payer": "9v8NmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 2},

    #                 {"signature": "256541659","time_stamp":123, "fee_payer": "10vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 2},
    #                 {"signature": "256541660","time_stamp":123, "fee_payer": "10vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 3},

    #                 {"signature": "256541661","time_stamp":123, "fee_payer": "11vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 3},

    #                 {"signature": "256541662","time_stamp":123, "fee_payer": "12vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 1},

    #                 {"signature": "256541671","time_stamp":123, "fee_payer": "16vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 1},
    #                 {"signature": "256541672","time_stamp":123, "fee_payer": "16vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 2},
    #                 {"signature": "2565411220","time_stamp":123, "fee_payer": "66vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 3},
                    


    #                                 # sell
    #                 {"signature": "256541663","time_stamp":123, "fee_payer": "13vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "DADDY" , "got_amount": 12, "got_token": "SOL", "status":"sell",  "set_number": 4},
    #                 {"signature": "256541664","time_stamp":123, "fee_payer": "8v8NmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "DADDY" , "got_amount": 12, "got_token": "SOL", "status":"sell",  "set_number": 5},
    #                 {"signature": "256541665","time_stamp":123, "fee_payer": "13vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "DADDY" , "got_amount": 12, "got_token": "SOL", "status":"sell",  "set_number": 6},
    #                 {"signature": "2565416666","time_stamp":123, "fee_payer": "13vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "DADDY" , "got_amount": 12, "got_token": "SOL", "status":"sell",  "set_number": 7},

    #                 {"signature": "2565416667","time_stamp":123, "fee_payer": "14vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "DADDY" , "got_amount": 12, "got_token": "SOL", "status":"sell",  "set_number": 4},
    #                 {"signature": "2565416668","time_stamp":123, "fee_payer": "14vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "DADDY" , "got_amount": 12, "got_token": "SOL", "status":"sell",  "set_number": 7},

    #                 {"signature": "2565416669","time_stamp":123, "fee_payer": "15vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "DADDY" , "got_amount": 12, "got_token": "SOL", "status":"sell",  "set_number": 7},

    #                 {"signature": "2565416670","time_stamp":123, "fee_payer": "16vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "DADDY" , "got_amount": 12, "got_token": "SOL", "status":"sell",  "set_number": 7},
    #                 {"signature": "2565416673","time_stamp":123, "fee_payer": "16vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "DADDY" , "got_amount": 12, "got_token": "SOL", "status":"sell",  "set_number": 4},
    #                 {"signature": "256541117","time_stamp":123, "fee_payer": "66vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "BILLY", "status":"sell",  "set_number": 5},




    #                 {"signature": "256541680","time_stamp":123, "fee_payer": "20vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "BILLY", "status":"buy",  "set_number": 8},
    #                 {"signature": "256541681","time_stamp":123, "fee_payer": "20vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "BILLY", "status":"buy",  "set_number": 9},

    #                 {"signature": "256541682","time_stamp":123, "fee_payer": "22vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "BILLY", "status":"buy",  "set_number": 8},

    #                 {"signature": "256541683","time_stamp":123, "fee_payer": "21vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "BILLY", "status":"buy",  "set_number": 8},
    #                 {"signature": "256541684","time_stamp":123, "fee_payer": "21vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "BILLY", "status":"buy",  "set_number": 9},


    #                 {"signature": "256541685","time_stamp":123, "fee_payer": "23vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "BILLY", "status":"buy",  "set_number": 8},

    #                 {"signature": "256541686","time_stamp":123, "fee_payer": "23vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "BILLY", "status":"buy",  "set_number": 9},

    #                 {"signature": "256541687","time_stamp":123, "fee_payer": "24vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "BILLY", "status":"buy",  "set_number": 9},

    #                 {"signature": "256541688","time_stamp":123, "fee_payer": "25vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "BILLY", "status":"buy",  "set_number": 9},
    #                 {"signature": "2565416966","time_stamp":123, "fee_payer": "16vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "BILLY", "status":"buy",  "set_number": 9},
    #                 {"signature": "256541118","time_stamp":123, "fee_payer": "66vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "BILLY", "status":"buy",  "set_number": 8},





    #                 {"signature": "256541689","time_stamp":123, "fee_payer": "23vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "BILLY", "status":"sell",  "set_number": 10},

    #                 {"signature": "256541690","time_stamp":123, "fee_payer": "23vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "BILLY", "status":"sell",  "set_number": 11},

    #                 {"signature": "256541691","time_stamp":123, "fee_payer": "25vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "BILLY", "status":"sell",  "set_number": 10},

    #                 {"signature": "256541692","time_stamp":123, "fee_payer": "26vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "BILLY", "status":"sell",  "set_number": 11},

    #                 {"signature": "256541693","time_stamp":123, "fee_payer": "27vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "BILLY", "status":"sell",  "set_number": 10},

    #                 {"signature": "256541694","time_stamp":123, "fee_payer": "27vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "BILLY", "status":"sell",  "set_number": 11},

    #                 {"signature": "256541695","time_stamp":123, "fee_payer": "16vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "BILLY", "status":"sell",  "set_number": 10},
    #                 {"signature": "256541117","time_stamp":123, "fee_payer": "66vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "BILLY", "status":"sell",  "set_number": 11},

    #                 {"signature": "2565411179","time_stamp":123, "fee_payer": "999vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "BILLY", "status":"sell",  "set_number": 4},
    #                 {"signature": "25654111799","time_stamp":123, "fee_payer": "999vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "BILLY", "status":"sell",  "set_number": 10},




    #                 {"signature": "256541696","time_stamp":123, "fee_payer": "288NmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "CHAD", "status":"buy",  "set_number": 12},
    #                 {"signature": "256541697","time_stamp":123, "fee_payer": "288NmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":13, "sold_token": "SOL" , "got_amount": 12, "got_token": "CHAD", "status":"buy",  "set_number": 13},
    #                 {"signature": "256541698","time_stamp":123, "fee_payer": "288NmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":14, "sold_token": "SOL" , "got_amount": 12, "got_token": "CHAD", "status":"buy",  "set_number": 14},


    #                 {"signature": "256541699","time_stamp":123, "fee_payer": "298NmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "CHAD", "status":"buy",  "set_number": 12},
    #                 {"signature": "256541100","time_stamp":123, "fee_payer": "298NmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "CHAD", "status":"buy",  "set_number": 13},

    #                 {"signature": "256541101","time_stamp":123, "fee_payer": "30vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "CHAD", "status":"buy",  "set_number": 13},
    #                 {"signature": "256541102","time_stamp":123, "fee_payer": "30vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "CHAD", "status":"buy",  "set_number": 14},

    #                 {"signature": "256541103","time_stamp":123, "fee_payer": "31vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "CHAD", "status":"buy",  "set_number": 12},

    #                 {"signature": "256541104","time_stamp":123, "fee_payer": "32vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "CHAD", "status":"buy",  "set_number": 13},

    #                 {"signature": "256541105","time_stamp":123, "fee_payer": "33vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "CHAD", "status":"buy",  "set_number": 12},

    #                 {"signature": "256541106","time_stamp":123, "fee_payer": "16vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "CHAD", "status":"buy",  "set_number": 14},
    #                 {"signature": "256541116","time_stamp":123, "fee_payer": "66vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "CHAD", "status":"buy",  "set_number": 12},
                    
                    
                    
                    
    #                 {"signature": "256541107","time_stamp":123, "fee_payer": "348NmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "CHAD", "status":"sell",  "set_number": 15},
    #                 {"signature": "256541109","time_stamp":123, "fee_payer": "348NmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "CHAD", "status":"sell",  "set_number": 16},

    #                 {"signature": "256541108","time_stamp":123, "fee_payer": "35vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "CHAD", "status":"sell",  "set_number": 15},
    #                 {"signature": "256541110","time_stamp":123, "fee_payer": "35vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "CHAD", "status":"sell",  "set_number": 16},

    #                 {"signature": "256541111","time_stamp":123, "fee_payer": "36vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "CHAD", "status":"sell",  "set_number": 16},

    #                 {"signature": "256541112","time_stamp":123, "fee_payer": "37vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "CHAD", "status":"sell",  "set_number": 15},

    #                 {"signature": "256541113","time_stamp":123, "fee_payer": "38vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "CHAD", "status":"sell",  "set_number": 16},

    #                 {"signature": "256541114","time_stamp":123, "fee_payer": "16vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "CHAD", "status":"sell",  "set_number": 15},
    #                 {"signature": "256541115","time_stamp":123, "fee_payer": "66vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "CHAD", "status":"sell",  "set_number": 16},



    #             ]


            # data23 = [

            #     #coin1
            #     ## buy
            #     {"signature": "256541654","time_stamp":123, "fee_payer": "8v8NmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 1},
            #     {"signature": "256541655","time_stamp":123, "fee_payer": "8v8NmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":13, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 2},
            #     {"signature": "256541656","time_stamp":123, "fee_payer": "8v8NmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":14, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 3},

            #     {"signature": "256541657","time_stamp":123, "fee_payer": "9v8NmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 1},
            #     {"signature": "256541658","time_stamp":123, "fee_payer": "9v8NmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 2},

            #     {"signature": "256541659","time_stamp":123, "fee_payer": "10vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 2},
            #     {"signature": "256541660","time_stamp":123, "fee_payer": "10vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 3},

            #     {"signature": "256541661","time_stamp":123, "fee_payer": "11vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 3},

            #     {"signature": "256541662","time_stamp":123, "fee_payer": "12vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 1},

            #     {"signature": "256541671","time_stamp":123, "fee_payer": "16vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 1},

            #     {"signature": "256541672220","time_stamp":123, "fee_payer": "13vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"sell",  "set_number": 2},
            #     {"signature": "256541672330","time_stamp":123, "fee_payer": "14vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"sell",  "set_number": 2},
            #     {"signature": "256541672340","time_stamp":123, "fee_payer": "16vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"sell",  "set_number": 2},


            #     # sell
            #     {"signature": "256541663","time_stamp":123, "fee_payer": "13vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "DADDY" , "got_amount": 12, "got_token": "SOL", "status":"sell",  "set_number": 4},
            #     {"signature": "256541664","time_stamp":123, "fee_payer": "13vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "DADDY" , "got_amount": 12, "got_token": "SOL", "status":"sell",  "set_number": 5},
            #     {"signature": "256541665","time_stamp":123, "fee_payer": "13vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "DADDY" , "got_amount": 12, "got_token": "SOL", "status":"sell",  "set_number": 6},
            #     {"signature": "2565416666","time_stamp":123, "fee_payer": "13vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "DADDY" , "got_amount": 12, "got_token": "SOL", "status":"sell",  "set_number": 7},

            #     {"signature": "2565416667","time_stamp":123, "fee_payer": "14vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "DADDY" , "got_amount": 12, "got_token": "SOL", "status":"sell",  "set_number": 4},
            #     {"signature": "2565416668","time_stamp":123, "fee_payer": "14vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "DADDY" , "got_amount": 12, "got_token": "SOL", "status":"sell",  "set_number": 7},

            #     {"signature": "2565416669","time_stamp":123, "fee_payer": "15vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "DADDY" , "got_amount": 12, "got_token": "SOL", "status":"sell",  "set_number": 7},

            #     {"signature": "2565416670","time_stamp":123, "fee_payer": "16vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "DADDY" , "got_amount": 12, "got_token": "SOL", "status":"sell",  "set_number": 7},
            #     {"signature": "2565416673","time_stamp":123, "fee_payer": "16vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "DADDY" , "got_amount": 12, "got_token": "SOL", "status":"sell",  "set_number": 4},


            #     ## coin 2
            #     ## buy
            #     {"signature": "2565416545","time_stamp":123, "fee_payer": "8v8NmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 8},
            #     {"signature": "2565416555","time_stamp":123, "fee_payer": "8v8NmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":13, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 9},

            #     {"signature": "2565416575","time_stamp":123, "fee_payer": "9v8NmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 8},

            #     {"signature": "2565416595","time_stamp":123, "fee_payer": "10vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 9},

            #     {"signature": "2565416615","time_stamp":123, "fee_payer": "110vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 8},

            #     {"signature": "2565416625","time_stamp":123, "fee_payer": "120vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 9},

            #     {"signature": "2565416715","time_stamp":123, "fee_payer": "16vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 8},
            #     {"signature": "2565416725","time_stamp":123, "fee_payer": "16vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "SOL" , "got_amount": 12, "got_token": "DADDY", "status":"buy",  "set_number": 9},


            #     # sell
            #     {"signature": "2565416637","time_stamp":123, "fee_payer": "13vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "DADDY" , "got_amount": 12, "got_token": "SOL", "status":"sell",  "set_number": 10},
            #     {"signature": "2565416647","time_stamp":123, "fee_payer": "13vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "DADDY" , "got_amount": 12, "got_token": "SOL", "status":"sell",  "set_number": 11},
               

            #     {"signature": "25654166677","time_stamp":123, "fee_payer": "14vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "DADDY" , "got_amount": 12, "got_token": "SOL", "status":"sell",  "set_number": 10},

            #     {"signature": "25654166687","time_stamp":123, "fee_payer": "19vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "DADDY" , "got_amount": 12, "got_token": "SOL", "status":"sell",  "set_number": 10},

            #     {"signature": "25654166697","time_stamp":123, "fee_payer": "15vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "DADDY" , "got_amount": 12, "got_token": "SOL", "status":"sell",  "set_number": 11},

            #     {"signature": "25654166707","time_stamp":123, "fee_payer": "16vNmbqLyGU1uadp7UvCM6AqURUkdYMXDPUaA9nqNPNP", "action":"swap","sold_amount":12, "sold_token": "DADDY" , "got_amount": 12, "got_token": "SOL", "status":"sell",  "set_number": 10},



            #     ]
            
            # for x in data23:
            #         CoinTransactions.add_sample_transaction(x)


    #         k=1
    #         for y in data23:
    #             if k<=6:
    #                 CoinTransactions.add_new_transaction(y,1)
    #             elif k<=12:
    #                 CoinTransactions.add_new_transaction(y,2)
    #             elif k<=18:
    #                 CoinTransactions.add_new_transaction(y,3)
    #             elif k<=24:
    #                 CoinTransactions.add_new_transaction(y,4)
    #             elif k<=30:
    #                 CoinTransactions.add_new_transaction(y,5)
    #             elif k<=36 :
    #                 CoinTransactions.add_new_transaction(y,6)
    #             elif k<=41 :
    #                 CoinTransactions.add_new_transaction(y,7)
    #             elif k<=44 :
    #                 CoinTransactions.add_new_transaction(y,8)
    #             elif k<=49 :
    #                 CoinTransactions.add_new_transaction(y,9)
    #             elif k<=54 :
    #                 CoinTransactions.add_new_transaction(y,10)
    #             elif k<=59 :
    #                 CoinTransactions.add_new_transaction(y,11)
    #             elif k<=62 :
    #                 CoinTransactions.add_new_transaction(y,12)
    #             elif k<=66 :
    #                 CoinTransactions.add_new_transaction(y,13)
    #             elif k<=69 :
    #                 CoinTransactions.add_new_transaction(y,14)
    #             elif k<=71 :
    #                 CoinTransactions.add_new_transaction(y,15)
    #             elif k<=75 :
    #                 CoinTransactions.add_new_transaction(y,16)
    #             elif k<=79 :
    #                 CoinTransactions.add_new_transaction(y,17)
    #             elif k<=84 :
    #                 CoinTransactions.add_new_transaction(y,18)
    #             elif k<=88 :
    #                 CoinTransactions.add_new_transaction(y,19)
    #             else :
    #                 CoinTransactions.add_new_transaction(y,20)
    #             k=k+1


    # example out put

    # table_one_data = [
    #        
    #  coin 1 {
    #            "ticker": "daddy",
    #            "whales_count": 3,
    #            "no_of_sets": 3,
    #            "fee_payers": [
    #        whale 1  {"fee_payer": "Big4MGvf4dgmE6YNKegjcGBTkUvvVoi11Qrdw8BGMKen", "sets": [[1, 2, 3]]},
    #        whale 2  {"fee_payer": "RPW17KwHtGepfzCuzQsabxGTyPKMUDNwpNuLpBgUM3b", "sets": [[1, 2]]},
    #        whale 3  {"fee_payer": "9kDgyDEYGQCShMGMLDS7K9xTtHeWgmfyfYeF4YDTxx5m", "sets": [[2, 3]]}
    #            ]
    #          },
    #  coin 2  {
    #            "ticker": "mommy",
    #            "whales_count": 3,
    #            "no_of_sets": 2,
    #            "fee_payers": [
    #                 {"fee_payer": "Big4MGvf4dgmE6YNKegjcGBTkUvvVoi11Qrdw8BGMKen", "sets": [[4, 5]]},
    #                 {"fee_payer": "RPW17KwHtGepfzCuzQsabxGTyPKMUDNwpNuLpBgUM3b", "sets": [[4]]},
    #                 {"fee_payer": "9kDgyDEYGQCShMGMLDS7K9xTtHeWgmfyfYeF4YDTxx5m", "sets": [[5]]}
    #            ]
    #         }
    #     ]


# Table two data out put
    # table_two_data = [
    #     {
    #         'whale_asdress': 'Big4MGvf4dgmE6YNKegjcGBTkUvvVoi11Qrdw8BGMKen',
    #         'total_sets': [1, 2, 3, 4, 5],
    #         'coins': [
	# 	                {'ticker': 'daddy', 'coin_address': '4Cnk9EPnW5ixfLZatCPJjDB1PUtcRpVVgTQukm9epump', 'amount_of_sets': 3, 'whale_in_sets': [1, 2, 3]}, 
	# 	                {'ticker': 'monkey', 'coin_address': '9AvzWNZ5LN7MExZRbDCBj228wLEnR1svy7gfWkMRvEzz', 'amount_of_sets': 2, 'whale_in_sets': [4, 5]}
    #                 ]
    #     },
		
    #     {
    #         'whale_asdress': 'Kig4MGvf4dgmE6YNKegjcGBTkUvvVoi11Qrdw8BGMKen',
    #         'total_sets': [1, 2, 3, 4, 5],
    #         'coins': [
	# 	                {'ticker': 'daddy', 'coin_address': '4Cnk9EPnW5ixfLZatCPJjDB1PUtcRpVVgTQukm9epump', 'amount_of_sets': 3, 'whale_in_sets': [1, 2, 3]}, 
	# 	                {'ticker': 'monkey', 'coin_address': '9AvzWNZ5LN7MExZRbDCBj228wLEnR1svy7gfWkMRvEzz', 'amount_of_sets': 2, 'whale_in_sets': [4, 5]}
    #                 ]
    #     }
    # ]



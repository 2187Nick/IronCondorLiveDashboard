import os
import asyncio         
import csv
import pandas as pd
from datetime import datetime, timedelta, timezone
from td.client import TDClient
from datetime import datetime
import datetime
import time
import configparser
from deta import Deta

config = configparser.ConfigParser()
config.read('config.ini')

client_id = config['TDA']['ClientID']
redirect_uri = config['TDA']['RedirectURI']
credentials_path = config['TDA']['CredentialsPath']
account_number = config['TDA']['AccountNumber']
spx_discord_bot = config['DISCORD']['SPXDiscordBot']
detabase_key = config['DETA']['DetabaseKey']

TDSession = TDClient(
    client_id=client_id,
    redirect_uri=redirect_uri,
    credentials_path=credentials_path,
    account_number=account_number
)

def get_time_now():
    curr_clock = time.strftime("%H:%M:%S", time.localtime())
    int_curr_clock = int(f'{curr_clock[:2]}{curr_clock[3:5]}')

    return int_curr_clock 

async def close_trade(
        width,
        total_credit,
        contracts,
        sell_call_strike,
        sell_put_strike,
        call_midpoint,
        call_plus_width_midpoint,
        put_midpoint,
        put_minus_width_midpoint,
        left_wing_debit,
        right_wing_debit):

        retry_count = 0
        max_retries = 5

        while retry_count < max_retries:

            try:

                time_now = datetime.datetime.now()
                exit_time = time_now.strftime("%H:%M")
                print("Exit Time: ", exit_time) 
                print("condor_width: ", width)
                

                if get_time_now() > 1600:
                    # I need to check if we closed between the main strikes.
                    # If we did, then I can set left_wing_debit and right_wing_debit to 0
                    spx_quote = TDSession.get_quotes(instruments=['$SPX.X'])

                    spx_close_price = spx_quote['$SPX.X']['closePrice']
                    print("spx_close_price: ", spx_close_price)

                    if spx_close_price <= int(sell_call_strike) and spx_close_price >= int(sell_put_strike):
                        left_wing_debit = 0
                        right_wing_debit = 0
                        total_pay_to_close_both_wings = 0
                        print("total_pay_to_close_both_wings: ", total_pay_to_close_both_wings) 
                    
                    elif spx_close_price > int(sell_call_strike):
                        # Calculate the debit for the right wing
                        total_pay_to_close_both_wings = round(spx_close_price - int(sell_call_strike), 2)
                        print("total_pay_to_close_both_wings: ", total_pay_to_close_both_wings) 
                    
                    else:

                        # Calculate the debit for the left wing
                        total_pay_to_close_both_wings = round(int(sell_put_strike) - spx_close_price, 2)
                        print("total_pay_to_close_both_wings: ", total_pay_to_close_both_wings) 
                    
                else:

                    # Calculate the total paid to close both wings
                    total_pay_to_close_both_wings = round(left_wing_debit + right_wing_debit, 2)
                    print("total_pay_to_close_both_wings: ", total_pay_to_close_both_wings)

                        
                # Calculate profit for the trade.
                # Amount we received in credit - amount we paid to close the trade
                # total_credit will be an input value from the entry script

                # Setting this manually for testing
                #total_credit = 1

                profit = round(total_credit - total_pay_to_close_both_wings, 2) * 100

                trade_profit = round(profit * contracts, 0)

                print('######################################################')
                print(' ')

                print("Call Wing:")
                print("Buy: ", str(sell_call_strike) + "C @ $" + str(call_midpoint))
                print("Sell: ", str(sell_call_strike + width) + "C @ $" + str(call_plus_width_midpoint))
                print("Debit: $" + str(right_wing_debit))

                print(' ')
                print('######################################################')
                print(' ')

                print("Put Wing:")
                print("Buy: " + str(sell_put_strike) + "P @ $" + str(put_midpoint))
                print("Sell: " + str(sell_put_strike - width) + "P @ $" + str(put_minus_width_midpoint))
                print("Debit: $" + str(left_wing_debit))

                print(' ')
                print('######################################################')
                print(' ')

                print("Initial Credit: $" + str(total_credit))
                print("Debit Paid to Close Trade: $" + str(total_pay_to_close_both_wings))
                print("Profit: $" + str(profit))
                print("Trade Profit: $" + str(trade_profit))

                ######## Add the data to Deta Base ########
                deta = Deta(detabase_key)
                db = deta.Base("Condor")

                exp_today = str(datetime.datetime.now().date()) #  + datetime.timedelta(days=1))
                #exp_today = str(datetime.datetime.now().date()) 

                # Update the database when the trade is closed
                db.update({

                        'EXIT_TIME': exit_time,
                        'CALL_STRIKE0_CLOSE': call_midpoint,
                        'CALL_STRIKE1_CLOSE': call_plus_width_midpoint,
                        'CALL_WING_CLOSE': right_wing_debit,
                        'PUT_STRIKE0_CLOSE': put_midpoint,
                        'PUT_STRIKE1_CLOSE': put_minus_width_midpoint,
                        'PUT_WING_CLOSE': left_wing_debit,
                        'TOTAL_DEBIT_CLOSE': total_pay_to_close_both_wings,
                        'PROFIT': profit,
                        'TRADE_PROFIT': trade_profit
                    
                }, "condor_" + str(width) + "_" + exp_today)

                # Strategy Performance Database
                db_strat = deta.Base("StrategyPerformance")

                # Function to get the most recent balance for a specific strategy
                def get_most_recent_balance(strategy_id):
                    today = datetime.datetime.now().strftime("%Y-%m-%d")
                    query = {"strategy_id": strategy_id}
                    result = db_strat.fetch(query).items

                    if result:
                        # Filter out today's record and sort the rest by date in descending order
                        filtered_records = [record for record in result if record['date'] != today]
                        sorted_records = sorted(filtered_records, key=lambda x: x['date'], reverse=True)
                        
                        # Return the current balance of the most recent record
                        return sorted_records[0].get("current_balance") if sorted_records else None
                    else:
                        # If there are no records, return the starting balance
                        return 25000

                # Example usage: Get the most recent balance for "Strategy10" (excluding today)
                most_recent_balance = get_most_recent_balance(("Strategy" + str(width)))
                #most_recent_balance = 25000

                def update_performance(exp_today, width, starting_balance, most_recent_balance, trade_profit):
                    key = f"{exp_today}_{width}"
                    current_balance = most_recent_balance + trade_profit

                    return db_strat.put({
                        "DATE": exp_today,
                        "STRATEGY_ID": ("Strategy" + str(width)),
                        "STARTING_BALANCE": starting_balance,
                        "CURRENT_BALANCE": current_balance,
                        "PROFIT": trade_profit,
                        "TOTAL_PROFIT": round(current_balance - starting_balance,0 )}, key)
                
                update_performance(
                    exp_today,
                    width,
                    25000,
                    most_recent_balance,
                    trade_profit
                )

                # update the csv file
                def update_csv(file_path, new_data):
                    df = pd.read_csv(file_path)
                    for key, value in new_data.items():
                        df[key] = value
                    df.to_csv(file_path, index=False)

                # Usage example:
                file_path = str('storage/ic_' + str(width) + '_'  +exp_today+'.csv')
                new_data = {
                    "EXIT_TIME'": exit_time,
                    "CALL_STRIKE0_CLOSE": call_midpoint,
                    "CALL_STRIKE1_CLOSE": call_plus_width_midpoint,
                    "CALL_WING_CLOSE": right_wing_debit,
                    "PUT_STRIKE0_CLOSE": put_midpoint,
                    "PUT_STRIKE1_CLOSE": put_minus_width_midpoint,
                    "PUT_WING_CLOSE": left_wing_debit,
                    "TOTAL_DEBIT_CLOSE": total_pay_to_close_both_wings,
                    "PROFIT": profit,
                    "TRADE_PROFIT": trade_profit
                }
                update_csv(file_path, new_data)
                # If the script completes without raising an exception, break out of the loop
                break

            except Exception as e:
                print(f"An error occurred while closing trade: {e}")
                retry_count += 1
                print(f"Retrying... ({retry_count}/{max_retries})")

        if retry_count == max_retries:
            print("Maximum number of retries reached. The script could not complete successfully.")
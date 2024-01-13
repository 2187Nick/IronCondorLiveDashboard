import os
import asyncio         
import csv
import pandas as pd
from datetime import datetime, timedelta, timezone
from td.client import TDClient
from datetime import datetime
import datetime
import time
import math
import configparser
from deta import Deta

import three_condors_monitor_stoploss

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

start_date = datetime.datetime.now().date()  # + datetime.timedelta(days=1)
end_date = datetime.datetime.now().date()  # + datetime.timedelta(days=1)
print("start_date: " , start_date)
exp_today = str(datetime.datetime.now().date()) #  + datetime.timedelta(days=1)
dte=start_date-datetime.date.today()


def get_time_now():
    curr_clock = time.strftime("%H:%M:%S", time.localtime())
    int_curr_clock = int(f'{curr_clock[:2]}{curr_clock[3:5]}')

    return int_curr_clock 

#start_time = 933

spx_quote = TDSession.get_quotes(instruments=['$SPX.X'])
opt_lookup = TDSession.get_options_chain(option_chain={'symbol': ('$SPX.X'), 'fromDate': start_date, 'toDate': end_date, 'strikeCount': 100}) 
callMap = opt_lookup['callExpDateMap'][exp_today+":"+str(dte.days)]
putMap = opt_lookup['putExpDateMap'][exp_today+":"+str(dte.days)]
#print("callMap: ", callMap)

# round spx price to nearest 0
spx_price = round(spx_quote['$SPX.X']['lastPrice'], -1)
print("spx_price_last: ", spx_price)


# Manual spx price for testing
#spx_price = 4755

# 0.5% of spx price = .005
percentage = 0.0075


#percentage = 0.005
#percentage = 0.0001


# 1% above spx price
sell_call_strike = round(spx_price * (1 + percentage), -1)
#print("sell_call_strike: ", sell_call_strike)
#print("buy_call_strike: ", sell_call_strike + width) 

# 1% below spx price
sell_put_strike = round(spx_price * (1 - percentage), -1)
#print("sell_put_strike: ", sell_put_strike)
#print("buy_put_strike: ", sell_put_strike - width)


################# This version attempts to caclulate the midepoint of the spread #################
# Get the bid price for the call
call_bid_price = opt_lookup['callExpDateMap'][exp_today+":"+str(dte.days)][str(sell_call_strike)][0]['bid']
#print("call_bid_price: ", call_bid_price)

#get the ask price for the call
call_ask_price = opt_lookup['callExpDateMap'][exp_today+":"+str(dte.days)][str(sell_call_strike)][0]['ask']
#print("call_ask_price: ", call_ask_price)

# If the ask is less than .10, then use .05 as the midpoint
# round the midpoint down to the nearest 0.05
if call_ask_price >= .10:
    call_midpoint = round(math.floor(((call_ask_price + call_bid_price) / 2) / .05) * .05, 2)
    #print("call_midpoint: ", call_midpoint)

else:
    call_midpoint = .05
    #print("call_midpoint: ", call_midpoint)

#breakpoint()

put_bid_price = opt_lookup['putExpDateMap'][exp_today+":"+str(dte.days)][str(sell_put_strike)][0]['bid']
#print("put_bid_price: ", put_bid_price)

put_ask_price = opt_lookup['putExpDateMap'][exp_today+":"+str(dte.days)][str(sell_put_strike)][0]['ask']
#print("put_ask_price: ", put_ask_price)

# If the ask is less than .10, then use .05 as the midpoint
if put_ask_price >= .10:
    put_midpoint = round(math.floor(((put_ask_price + put_bid_price) / 2) / .05) * .05, 2)
    #print("put_midpoint: ", put_midpoint)

else:
    put_midpoint = .05
    #print("put_midpoint: ", put_midpoint)

#### All the spread sell the same put and call strikes ####
#### Here I need a loop to calculate the midpoint for the 10, 20 and 30 point wings ####

spread_widths = [10, 20, 30]
trade_list = []

for width in spread_widths:
    call_plus_width_ask_price = opt_lookup['callExpDateMap'][exp_today+":"+str(dte.days)][str(sell_call_strike+width)][0]['ask']
    print("call_plus{}_ask_price: ".format(width), call_plus_width_ask_price)

    call_plus_width_bid_price = opt_lookup['callExpDateMap'][exp_today+":"+str(dte.days)][str(sell_call_strike+width)][0]['bid']
    print("call_plus{}_bid_price: ".format(width), call_plus_width_bid_price)

    put_minus_width_ask_price = opt_lookup['putExpDateMap'][exp_today+":"+str(dte.days)][str(sell_put_strike-width)][0]['ask']
    print("put_minus{}_ask_price: ".format(width), put_minus_width_ask_price)

    put_minus_width_bid_price = opt_lookup['putExpDateMap'][exp_today+":"+str(dte.days)][str(sell_put_strike-width)][0]['bid']
    print("put_minus{}_bid_price: ".format(width), put_minus_width_bid_price)

    if call_plus_width_ask_price >= 0.10:
        call_plus_width_midpoint = round(math.ceil(((call_plus_width_ask_price + call_plus_width_bid_price) / 2) / .05) * .05, 2)
        print("call_plus{}_midpoint: ".format(width), call_plus_width_midpoint)

    else:
        call_plus_width_midpoint = .05
        print("call_plus{}_midpoint: ".format(width), call_plus_width_midpoint)

    if put_minus_width_ask_price >= 0.10:
        put_minus_width_midpoint = round(math.ceil(((put_minus_width_ask_price + put_minus_width_bid_price) / 2) / .05) * .05, 2)
        print("put_minus_width_midpoint: ", put_minus_width_midpoint)

    else:
        put_minus_width_midpoint = .05
        print("put_minus_width_midpoint: ", put_minus_width_midpoint)

    # Calculate the 30 point wing credit based on midpoint
    left_wing30_credit = round(put_midpoint - put_minus_width_midpoint, 2)
    print("left_wing30_credit: ", left_wing30_credit)

    right_wing30_credit = round(call_midpoint - call_plus_width_midpoint, 2)
    print("right_wing30_credit: ", right_wing30_credit)

    # Calculate the total credit for the 30 point wings
    total_credit = round(left_wing30_credit + right_wing30_credit, 2)
    print("total_credit: ", total_credit)

    # Each strategy will sell a different # of contracts based on the total credit
    # $10 wide strategy sells 15 contracts
    # $20 wide strategy sells 7 contracts
    # $30 wide strategy sells 5 contracts
    if width == 10:
        contracts = 15  
    elif width == 20:
        contracts = 7
    else:
        contracts = 5

    total_prem_rec = round(total_credit * contracts * 100, 0)

    # Calculate the stop loss for the 30 point wings. This is 5x the total credit
    stop_loss = round(total_credit * 5, 2)

    print('######################################################')
    print(' ')

    print("Call Wing:")
    print("Sell: ", str(sell_call_strike) + "C @ $" + str(call_midpoint))
    print("Buy: ", str(sell_call_strike + width) + "C @ $" + str(call_plus_width_midpoint))
    print("Credit: $" + str(right_wing30_credit))

    print(' ')
    print('######################################################')
    print(' ')

    print("Put Wing:")
    print("Sell: " + str(sell_put_strike) + "P @ $" + str(put_midpoint))
    print("Buy: " + str(sell_put_strike - width) + "P @ $" + str(put_minus_width_midpoint))
    print("Credit: $" + str(left_wing30_credit))

    print(' ')
    print('######################################################')
    print(' ')

    print("Total Credit: $" + str(total_credit))

    print('Total Premium Received: ', total_prem_rec)

    print("Stop_Loss: $" + str(stop_loss))

    # Every time the script runs I want to write the data to a csv file
    # I want to write the data to a new csv file

    # Create the csv file for today
    filename = str('storage/ic_' + str(width) + '_'  +exp_today+'.csv')
    fields = [
        'DATE',
        'ENTRY_TIME',
        'SPX_PRICE',
        'PUT_STRIKE0',
        'PUT_STRIKE0_SELL',
        'PUT_STRIKE0_CLOSE',
        'PUT_STRIKE1',
        'PUT_STRIKE1_BUY',
        'PUT_STRIKE1_CLOSE',
        'PUT_WING_CREDIT',
        'PUT_WING_CLOSE',
        'CALL_STRIKE0',
        'CALL_STRIKE0_SELL',
        'CALL_STRIKE0_CLOSE',
        'CALL_STRIKE1',
        'CALL_STRIKE1_BUY',
        'CALL_STRIKE1_CLOSE',
        'CALL_WING_CREDIT',
        'CALL_WING_CLOSE',
        'STOP_LOSS',
        'TOTAL_CREDIT',
        'CONTRACTS',
        'TOTAL_DEBIT_CLOSE',
        'EXIT_TIME',
        'PROFIT',
        'TRADE_PROFIT'

    ]

    # if the file does not exit, create it
    if not os.path.isfile(filename):
        # writing to csv file 
        with open(filename, 'w') as csvfile: 
            # creating a csv writer object 
            csvwriter = csv.writer(csvfile) 
            # writing the fields 
            csvwriter.writerow(fields) 

    time_now = datetime.datetime.now()
    date = time_now.strftime("%m/%d/%Y")
    time_hhmm = time_now.strftime("%H:%M")
    print("Time", time_hhmm) 

    rows = [[
        date,
        time_hhmm,
        spx_price,
        sell_put_strike, 
        put_midpoint, 
        0,# close price
        sell_put_strike - width, 
        put_minus_width_midpoint,
        0,# close price, 
        left_wing30_credit, 
        0, # left_wing_close_price 
        sell_call_strike, 
        call_midpoint, 
        0,# close price
        sell_call_strike + width, 
        call_plus_width_midpoint, 
        right_wing30_credit, 
        0, # right_wing_close_price 
        stop_loss, 
        total_credit, 
        contracts,
        0, # total_debit_close_price
        "", # exit_time
        0, # profit
        0, # trade_profit
    ]]

    # writing to csv file 
    with open(filename, 'a') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
        # writing the data rows 
        csvwriter.writerows(rows)

    ######## Add the data to Deta Base ########
    deta = Deta(detabase_key)
    db = deta.Base("Condor")

    db.put({
    
        'DATE': date,
        'ENTRY_TIME': time_hhmm,
        'EXIT_TIME': "",
        'SPX_PRICE': spx_price,
        'PUT_STRIKE0': sell_put_strike,
        'PUT_STRIKE0_SELL': put_midpoint,
        'PUT_STRIKE0_CLOSE': "",
        'PUT_STRIKE1':  (sell_put_strike - width),
        'PUT_STRIKE1_BUY':  put_minus_width_midpoint,
        'PUT_STRIKE1_CLOSE':  "",
        'PUT_WING_CREDIT':  left_wing30_credit,
        'PUT_WING_CLOSE':  "",
        'CALL_STRIKE0':  sell_call_strike,
        'CALL_STRIKE0_SELL':  call_midpoint,
        'CALL_STRIKE0_CLOSE':  "",
        'CALL_STRIKE1':  (sell_call_strike + width),
        'CALL_STRIKE1_BUY':  call_plus_width_midpoint,
        'CALL_STRIKE1_CLOSE':  "",
        'CALL_WING_CREDIT':  right_wing30_credit,
        'CALL_WING_CLOSE':   "",
        'STOP_LOSS': stop_loss,
        'TOTAL_CREDIT': total_credit,
        'CONTRACTS': contracts,
        'TOTAL_DEBIT_CLOSE': "",
        'PROFIT': "",
        'TRADE_PROFIT': ''

    }, ("condor_"+ str(width) + "_" + exp_today))

    trade = {
        'width': width,
        'stop_loss': stop_loss, 
        'total_credit': total_credit, 
        'contracts': contracts,
        'sell_call_strike': sell_call_strike, 
        'sell_put_strike': sell_put_strike, 
        'call_midpoint': call_midpoint, 
        'call_plus_width_midpoint': call_plus_width_midpoint, 
        'put_midpoint': put_midpoint, 
        'put_minus_width_midpoint': put_minus_width_midpoint, 
    }

    trade_list.append(trade)

    
async def main():
    # Initialize your trades here
    trade1 = trade_list[0]
    trade2 = trade_list[1]
    trade3 = trade_list[2]

    # Start monitoring each trade concurrently
    # **trade unpacks the dictionary into keyword arguments
    try:
        await asyncio.gather(
            three_condors_monitor_stoploss.monitor_trade(**trade1),
            three_condors_monitor_stoploss.monitor_trade(**trade2),
            three_condors_monitor_stoploss.monitor_trade(**trade3)
        )
    except Exception as e:
        print(f"An error occurred: {e}")


asyncio.run(main())
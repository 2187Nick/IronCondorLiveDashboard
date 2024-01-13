import asyncio 
import sys        
from datetime import datetime, timedelta, timezone
from td.client import TDClient
from datetime import datetime
import datetime
import time
import math
import configparser
from three_condors_close_trade import close_trade

async def monitor_trade(
    width,
    stop_loss, 
    total_credit,
    contracts,
    sell_call_strike,
    sell_put_strike,
    call_midpoint,
    call_plus_width_midpoint,
    put_midpoint,
    put_minus_width_midpoint,
    ):

    try:
        print(f"Started monitoring condor {width} trade")

        config = configparser.ConfigParser()
        config.read('config.ini')
        client_id = config['TDA']['ClientID']
        redirect_uri = config['TDA']['RedirectURI']
        credentials_path = config['TDA']['CredentialsPath']
        account_number = config['TDA']['AccountNumber']

        TDSession = TDClient(
            client_id=client_id,
            redirect_uri=redirect_uri,
            credentials_path=credentials_path,
            account_number=account_number
        )

        start_date = datetime.datetime.now().date()  # + datetime.timedelta(days=1)
        end_date = datetime.datetime.now().date()  # + datetime.timedelta(days=1)
        print("start_date: " , start_date)
        exp_today = str(datetime.datetime.now().date()) #  + datetime.timedelta(days=1))
        dte=start_date-datetime.date.today()

        def get_time_now():
            curr_clock = time.strftime("%H:%M:%S", time.localtime())
            int_curr_clock = int(f'{curr_clock[:2]}{curr_clock[3:5]}')

            return int_curr_clock 

        end_time = 1600
        
        while get_time_now() < end_time:

            retry_count = 0
            max_retries = 5

            while retry_count < max_retries:

                try:

                    # I can change this to get the quotes for the option contracts. using underlyingsymbol quote.
                    spx_quote = TDSession.get_quotes(instruments=['$SPX.X'])
                    opt_lookup = TDSession.get_options_chain(option_chain={'symbol': ('$SPX.X'), 'fromDate': start_date, 'toDate': end_date, 'strikeCount': 100}) 
                    #callMap = opt_lookup['callExpDateMap'][exp_today+":"+str(dte.days)]
                    #putMap = opt_lookup['putExpDateMap'][exp_today+":"+str(dte.days)]

                    # round spx price to nearest 0
                    spx_price = round(spx_quote['$SPX.X']['lastPrice'], 2)
                    print("spx_price_last: ", spx_price)

                    # Manual spx price for testing
                    """ spx_price = 4700 """


                    ################# This attempts to caclulate the midpoint of the Call spread #################

                    # We are closing this trade. We initially received a credit. Now we are buying to close for a debit.
                    # 4750C is the strike we sold. We need to buy it back for a debit. 
                    # So we need to round up to the nearest 0.05. We pay closer to the Ask price when we buy to close.

                    # Get the bid price for the call
                    call_bid_price = opt_lookup['callExpDateMap'][exp_today+":"+str(dte.days)][str(sell_call_strike)][0]['bid']
                    #print("call_bid_price: ", call_bid_price)

                    #get the ask price for the call
                    call_ask_price = opt_lookup['callExpDateMap'][exp_today+":"+str(dte.days)][str(sell_call_strike)][0]['ask']
                    #print("call_ask_price: ", call_ask_price)

                    # If the ask is less than .10, then use .05 as the midpoint
                    # round the midpoint down to the nearest 0.05
                    if call_ask_price >= .10:
                        call_midpoint = round(math.ceil(((call_ask_price + call_bid_price) / 2) / .05) * .05, 2)
                        #print("call_midpoint: ", call_midpoint)

                    else:
                        call_midpoint = .05
                        #print("call_midpoint: ", call_midpoint)

                    call_plus_width_ask_price = opt_lookup['callExpDateMap'][exp_today+":"+str(dte.days)][str(sell_call_strike+width)][0]['ask']
                    #print("call_plus_width_ask_price: ", call_plus_width_ask_price)

                    call_plus_width_bid_price = opt_lookup['callExpDateMap'][exp_today+":"+str(dte.days)][str(sell_call_strike+width)][0]['bid']
                    #print("call_plus_width_bid_price: ", call_plus_width_bid_price)

                    #Example. 4780C. The bid is 0.05 and the ask is 0.10. I need to pay 0.05 to close the trade.
                    # We are closing this trade. We initially went long for a debit. Now we are selling to close for a credit.
                    # So we need to round down to the nearest 0.05. We receive closer to the Bid price when we sell to close.

                    # If the ask is less than .10, then use .05 as the midpoint
                    # round the midpoint down to the nearest 0.05
                    # calculate the midpoint for the 30 point wings
                    if call_plus_width_ask_price >= 0.10:
                        call_plus_width_midpoint = round(math.floor(((call_plus_width_ask_price + call_plus_width_bid_price) / 2) / .05) * .05, 2)
                        #print("call_plus_width_midpoint: ", call_plus_width_midpoint)

                    else:
                        call_plus_width_midpoint = .05
                        #print("call_plus_width_midpoint: ", call_plus_width_midpoint)

                    # We are closing this trade. We initially received a credit. Now we are buying to close for a debit.
                    # 4750C is the strike we sold. We need to buy it back for a debit. 
                    # 4780C is the strike we bought. We need to sell it for a credit.
                    # We initially received a credit of $1.00. We need to pay $0.50 to close the trade.
                    # 4750C we buy it to close for a debit of .70. 
                    # We sell 4780C for a credit of .20.
                    # .70 - .20 = .50
                    right_wing_debit = round(call_midpoint - call_plus_width_midpoint, 2)
                    print("right_wing_debit: ", right_wing_debit)


                    ################# This attempts to caclulate the midpoint of the Put spread when exiting trade #################
                        
                    put_bid_price = opt_lookup['putExpDateMap'][exp_today+":"+str(dte.days)][str(sell_put_strike)][0]['bid']
                    #print("put_bid_price: ", put_bid_price)

                    put_ask_price = opt_lookup['putExpDateMap'][exp_today+":"+str(dte.days)][str(sell_put_strike)][0]['ask']
                    #print("put_ask_price: ", put_ask_price)

                    # Here we are closing the trade. We initially sold for credit. 
                    # Now we are buying to close for a debit. So we need to round up to the nearest 0.05. 
                    # We pay closer to the Ask price when we buy to close.

                    # if im closing out 4700P. The bid is 0.05 and the ask is 0.10. I need to pay 0.10 to close the trade.

                    # If the ask is less than .10, then use .05 as the midpoint
                    if put_ask_price >= .10:
                        put_midpoint = round(math.ceil(((put_ask_price + put_bid_price) / 2) / .05) * .05, 2)
                        #print("put_midpoint: ", put_midpoint)

                    else:
                        put_midpoint = .05
                        #print("put_midpoint: ", put_midpoint)

                    put_minus_width_ask_price = opt_lookup['putExpDateMap'][exp_today+":"+str(dte.days)][str(sell_put_strike-width)][0]['ask']
                    #print("put_minus_width_ask_price: ", put_minus_width_ask_price)

                    put_minus_width_bid_price = opt_lookup['putExpDateMap'][exp_today+":"+str(dte.days)][str(sell_put_strike-width)][0]['bid']
                    #print("put_minus_width_bid_price: ", put_minus_width_bid_price)

                    #Example. 4680P. The bid is 0.05 and the ask is 0.10. I need to pay 0.05 to close the trade.
                    # We are closing this trade. We initially went long for a debit. Now we are selling to close for a credit.
                    # So we need to round down to the nearest 0.05. We receive closer to the Bid price when we sell to close.

                    if put_minus_width_ask_price >= 0.10:
                        put_minus_width_midpoint = round(math.floor(((put_minus_width_ask_price + put_minus_width_bid_price) / 2) / .05) * .05, 2)
                        #print("put_minus_width_midpoint: ", put_minus_width_midpoint)

                    else:
                        put_minus_width_midpoint = .05
                        #print("put_minus_width_midpoint: ", put_minus_width_midpoint)

                    # Calculate the wing debit based on midpoint EX:
                    # I need to buy to close 4700P for a debit of .50
                    # I need to sell to close 4670P for a credit of .20
                    left_wing_debit = round(put_midpoint - put_minus_width_midpoint, 2)
                    print("left_wing_debit: ", left_wing_debit)
                    

                    print("stop_loss: ", stop_loss)
                    print("condor width: ", width)
                    print("###############")
                    print("")

                    #### Now we check if the stoploss has been met by either wing ####
                    if (left_wing_debit >= stop_loss or right_wing_debit >= stop_loss):
                        print("Stoploss met. Break loop and activate close trade function.")
                        await close_trade(
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
                            right_wing_debit
                        )
                        sys.exit()  # End the script


                    print("sleep for 60 seconds")
                    await asyncio.sleep(60)

                except Exception as e:
                    print(f"An error occurred while closing trade: {e}")
                    retry_count += 1
                    print(f"Retrying... ({retry_count}/{max_retries})")

            if retry_count == max_retries:
                print("Maximum number of retries reached. The script could not complete successfully.")

        # If we make it to 16:01 then close the trade and send the close prices and profit loss to the deta detabase
        await close_trade(
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
            right_wing_debit
        )

    except Exception as e:
        print(f"An error occurred while monitoring trade {width}: {e}")
        


        

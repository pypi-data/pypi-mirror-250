import sys
from pathlib import Path

import json
# Add the project directory to the sys.path
project_dir = str(Path(__file__).resolve().parents[1])
if project_dir not in sys.path:
    sys.path.append(project_dir)
import os
from dotenv import load_dotenv
from fudstop._markets.list_sets.dicts import hex_color_dict
from apis.discord_.discord_sdk import DiscordSDK
from market_handlers.database_ import MarketDBManager
load_dotenv()
from discord_webhook import AsyncDiscordWebhook, DiscordEmbed
from monitor import EquityOptionTradeMonitor
from polygon.websocket import WebSocketClient, Market
from polygon.websocket.models import WebSocketMessage, EquityAgg,EquityQuote,EquityTrade,IndexValue
from fudstop.apis.polygonio.mapping import option_condition_desc_dict,option_condition_dict,OPTIONS_EXCHANGES,stock_condition_desc_dict,stock_condition_dict,indicators,quote_conditions,STOCK_EXCHANGES
from list_sets.dicts import all_forex_pairs, crypto_currency_pairs
# Create a reverse dictionary
all_forex_pairs = {v: k for k, v in all_forex_pairs.items()}
from typing import List
import asyncio
from asyncio import Queue
import pandas as pd
import logging
class MultiMarkets:
    def __init__(self, user, database, port, host, password):

        self.discord = DiscordSDK()
        self.db = MarketDBManager(user=user,database=database,port=port,host=host,password=password)
        self.markets = [Market.Options, Market.Stocks, Market.Crypto, Market.Forex, Market.Indices]# Market.Forex, Market.Indices]
        self.subscription_patterns = {
            Market.Options: ["T.*,A.*"],
            Market.Stocks: ["A.*,T.*"],
            Market.Indices: ["A.*"],
            Market.Crypto: ['XAS.*, XT.*'],
            Market.Forex: ['CAS.*']

        }


        self.created_channels = set()  # A set to keep track of created channels
        self.last_ticker = None
        self.consecutive_count = 0

    async def send_and_execute_webhook(self, hook: AsyncDiscordWebhook, embed: DiscordEmbed):
        hook.add_embed(embed)
        await hook.execute()

    async def create_channel_if_not_exists(self, ticker, name):
        # Check if the channel already exists
        if ticker not in self.created_channels:
            # If not, create the channel and add its name to the set
            await self.discord.create_channel(name=ticker, channel_description=name)
            self.created_channels.add(ticker)










    # Function to handle incoming WebSocket messages
            
    async def handle_msg(self, msgs: WebSocketMessage):
  
        monitor = EquityOptionTradeMonitor()
        
        for m in msgs:

         
            event_type = m.event_type
            if event_type == 'A' and m.symbol.startswith('I:'):
                async for data in self.db.insert_indices_aggs_second(m):
                    ticker = data.get('ticker')
                    last_five_trades = await monitor.repeated_hits(data)


                    if last_five_trades:
                        print(last_five_trades)


        
            if event_type == 'AM' and m.symbol.startswith('I:'):
                async for data in self.db.insert_indices_aggs_minute(m):
                    ticker = data.get('ticker')
                    print(ticker)




            #option aggs
            if event_type == 'A' and m.symbol.startswith('O:'):
                async for data in self.db.insert_option_aggs(m):
                    ticker = data.get('ticker')
                    print(ticker)



        

            #stock aggs
            if event_type == 'A' and not m.symbol.startswith('I:') and not m.symbol.startswith("O:"):
                async for data in self.db.insert_stock_aggs(m):
                    ticker = data.get('ticker')
                    print(ticker)






            if event_type == 'T' and m.symbol.startswith('O:'):
                async for data in self.db.insert_option_trades(m):
                    ticker = data.get('ticker')
                    print(ticker)
                    # Call the repeated_hits method
                    last_five_trades = await monitor.repeated_hits(data)

                    # Check if the ticker has appeared 5 times in a row
                    if last_five_trades == 5:
                        embed = DiscordEmbed(title='Repeated Stock Hits', description=f"# > ")
                        print(f"{ticker} has appeared 5 times in a row.")
                        hook = AsyncDiscordWebhook(os.environ.get('repeated_hits'))
                        hook.add_embed(embed)
                        await hook.execute()

            if event_type == 'T' and not m.symbol.startswith('O:') and not m.symbol.startswith('I:'):
                async for data in self.db.insert_stock_trades(m):
                    ticker = data.get('ticker')
                    print(ticker)
                    # Call the repeated_hits method
                    last_five_trades = await monitor.repeated_hits(data)
                    embed = DiscordEmbed(title='Repeated Stock Hits', description=f"# > {ticker}", color=hex_color_dict['gold'])
                    
                    if last_five_trades:
                        # Do something with the last five trades
                        print("Five consecutive trades found for ticker:", ticker)
                        print(last_five_trades)
                        counter = 0
                        for trade in last_five_trades:
                            counter = counter + 1
                            trade_type = trade['type']
                            ticker = trade['ticker']
                            trade_exchange = trade['trade_exchange']
                            trade_price = trade['trade_price']
                            trade_size = trade['trade_size']
                            trade_conditions = trade['trade_conditions']
                            embed.add_embed_field(name=f"Trade Info | {counter}", value=f"> Exchange: **{trade_exchange}**\n> Price: **${trade_price}**\n> Size: **{trade_size}**\n> Conditions: **{trade_conditions}**")
                        
                        print(f"{ticker} has appeared 5 times in a row.")
                        hook = AsyncDiscordWebhook(os.environ.get('repeated_hits'))
                        embed.set_timestamp()

                        asyncio.create_task(self.send_and_execute_webhook(hook, embed))
        




            if event_type == 'Q':
                async for data in self.db.insert_stock_quotes(m):
                    # Call the repeated_hits method
                    print(data.get('ticker'))

            if event_type == 'XT':
                async for data in self.db.insert_crypto_trades(m):
                    ticker = data.get('ticker')
                    print(ticker)
                    # Call the repeated_hits method
                    last_five_trades = await monitor.repeated_hits(data)

                    # Check if the ticker has appeared 5 times in a row
                    if last_five_trades == 5:
                        embed = DiscordEmbed(title='Repeated Stock Hits', description=f"# > {ticker}")
                        print(f"{ticker} has appeared 5 times in a row.")
                        hook = AsyncDiscordWebhook(os.environ.get('repeated_hits'))
                        hook.add_embed(embed)
                        await hook.execute()
                    

            if event_type == 'CAS':
                async for data in self.db.insert_forex_aggs(m=m):
                    ticker = data.get('ticker')
                    print(ticker)

                




market = MultiMarkets(host='localhost', user='chuck', database='markets', port=5432, password='fud')


async def main():
    await market.db.connect()
    while True:  # Restart mechanism
        try:
            await run_main_tasks()
        except Exception as e:
            print(e)
            logging.error(f"Critical error in main loop: {e}")
            logging.info("Restarting main loop...")
            await asyncio.sleep(10)  # Pause before restarting

# Main async function to connect to all markets with their respective subscriptions
async def run_main_tasks():

    clients = []
    for live_market in market.markets:
        patterns = market.subscription_patterns.get(live_market, [])
        for pattern in patterns:
            client = WebSocketClient(subscriptions=[pattern], api_key=os.environ.get('YOUR_POLYGON_KEY'), market=live_market)
            clients.append(client.connect(market.handle_msg))

    await asyncio.gather(*clients)  # Wait for all clients to finish



asyncio.run(main())

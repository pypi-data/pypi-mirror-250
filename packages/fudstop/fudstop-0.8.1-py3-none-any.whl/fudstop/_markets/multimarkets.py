import sys
from pathlib import Path
import json
# Add the project directory to the sys.path
project_dir = str(Path(__file__).resolve().parents[1])
if project_dir not in sys.path:
    sys.path.append(project_dir)
import os
from dotenv import load_dotenv
from apis.discord_.discord_sdk import DiscordSDK
from market_handlers.database_ import MarketDBManager
load_dotenv()
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
    def __init__(self):

        self.discord = DiscordSDK()
        self.db = MarketDBManager(user='chuck', database='fudstop')
        self.markets = [Market.Options, Market.Stocks, Market.Crypto, Market.Forex, Market.Indices]
        self.subscription_patterns = {
            Market.Options: ["T.*,A.*"],
            Market.Stocks: ["A.*,T.*,Q.*"],
            Market.Indices: ["A.*"],
            Market.Crypto: ['XAS.*, XT.*'],
            Market.Forex: ['CAS.*']

        }


        self.created_channels = set()  # A set to keep track of created channels

    async def create_channel_if_not_exists(self, ticker, name):
        # Check if the channel already exists
        if ticker not in self.created_channels:
            # If not, create the channel and add its name to the set
            await self.discord.create_channel(name=ticker, channel_description=name)
            self.created_channels.add(ticker)










    # Function to handle incoming WebSocket messages
    async def handle_msg(self, msgs: WebSocketMessage):
        
        for m in msgs:
            
            event_type = m.event_type
            if event_type == 'A' and m.symbol.startswith('I:'):
                async for m in self.db.insert_indices_aggs(m):
                    pass


            if event_type == 'A' and m.symbol.startswith('O:'):
                async for m in self.db.insert_option_aggs(m):
                    pass
        


            if event_type == 'A' and not m.symbol.startswith('I:') and not m.symbol.startswith("O:"):
                async for m in self.db.insert_stock_aggs(m):
                    print(m)





            if event_type == 'T' and m.symbol.startswith('O:'):
                async for m in self.db.insert_option_trades(m):
                    pass


            if event_type == 'T' and not m.symbol.startswith('O:') and not m.symbol.startswith('I:'):
                async for m in  self.db.insert_stock_trades(m):
                    pass






            if event_type == 'Q':
                async for m in self.db.insert_stock_quotes(m):
                    pass

            if event_type == 'XT':
                async for data in self.db.insert_crypto_trades(m):
                    
                    print(data)

                    

            if event_type == 'CAS':
                async for data in self.db.insert_forex_aggs(m=m):

                    name = all_forex_pairs.get(data['pair'])
                    

                    await self.discord.create_channel(guild_id=self.discord.fudstop_id, name=name, type='0', channel_description=f"Live forex from polygon.io! Go to https://www.polygon.io and use code FUDSTOP  at checkout for a 10% discount.> Forex Pair Monitored: {name} : Symbol: {data['pair']}")


market = MultiMarkets()


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
    await asyncio.gather(*clients)

# Run the main function
asyncio.run(main())

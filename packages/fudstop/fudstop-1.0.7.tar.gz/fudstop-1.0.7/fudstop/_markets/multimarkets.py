import sys
from pathlib import Path

import json
# Add the project directory to the sys.path
project_dir = str(Path(__file__).resolve().parents[1])
if project_dir not in sys.path:
    sys.path.append(project_dir)
import os
from asyncpg.exceptions import UniqueViolationError
from aiohttp.client_exceptions import ContentTypeError
from collections import deque
from dotenv import load_dotenv
from embeddings import vol_anal_embed, create_newhigh_embed, profit_ratio_02_embed, profit_ratio_98_embed, option_condition_embed, sized_trade_embed
from _markets.list_sets.dicts import hex_color_dict
from apis.discord_.discord_sdk import DiscordSDK
from _markets.list_sets.ticker_lists import most_active_tickers
from analyzers import OptionDataAnalyzer
from market_handlers.database_ import MarketDBManager
from _markets.market_handlers.list_sets import indices_names_and_symbols_dict, CRYPTO_DESCRIPTIONS,CRYPTO_HOOKS
load_dotenv()
from discord_webhook import AsyncDiscordWebhook, DiscordEmbed
from monitor import EquityOptionTradeMonitor
from polygon.websocket import WebSocketClient, Market
from polygon.websocket.models import WebSocketMessage, EquityAgg,EquityQuote,EquityTrade,IndexValue
from fudstop.apis.polygonio.mapping import option_condition_desc_dict,option_condition_dict,OPTIONS_EXCHANGES,stock_condition_desc_dict,stock_condition_dict,indicators,quote_conditions,STOCK_EXCHANGES
from list_sets.dicts import all_forex_pairs, crypto_currency_pairs
from apis.polygonio.technicals import Technicals
from apis.webull.webull_trading import WebullTrading
# Create a reverse dictionary
all_forex_pairs = {v: k for k, v in all_forex_pairs.items()}
from typing import List
import asyncio
import time
from asyncio import Queue
import pandas as pd
import logging
from _markets.webhook_dicts import option_conditions_hooks
from apis.polygonio.async_polygon_sdk import Polygon
from apis.polygonio.polygon_options import PolygonOptions
class MultiMarkets:
    def __init__(self, user, database, port, host, password):
        self.poly = Polygon(host='localhost', user='chuck', database='markets', password='fud', port=5432)
        self.discord = DiscordSDK()

        self.technicals = Technicals()
        self.db = MarketDBManager(user=user,database=database,port=port,host=host,password=password)
        self.markets = [Market.Options, Market.Stocks, Market.Indices]
        self.subscription_patterns = {
            Market.Options: ["T.*,A.*"],
            Market.Stocks: ["A.*,T.*"],
            Market.Indices: ["A.*"],
           # Market.Crypto: ['XT.*'],
            #Market.Forex: ['CAS.*']

        }
        self.ticker_cache = {}
        self.trading = WebullTrading()
        self.time_day = 'day'
        self.time_hour = 'hour'
        self.time_minute = 'minute'
        self.time_week = 'week'
        self.time_month='month'
        self.queue = asyncio.Queue()
        self.analyzer = OptionDataAnalyzer()
        self.ticker_queue = asyncio.Queue()
        self.created_channels = set()  # A set to keep track of created channels
        self.last_ticker = None
        self.consecutive_count = 0
        self.indices_names=indices_names_and_symbols_dict
        self.agg_tickers = deque(maxlen=250)
        self.trade_tickers = deque(maxlen=250)
        self.opts = PolygonOptions(user='chuck', database='markets', host='localhost', port=5432, password='fud')


    # Function to check if the stock should be processed
    def should_process_stock(self, ticker):
        current_time = time.time()
        if ticker in self.ticker_cache and current_time - self.ticker_cache[ticker] < 60:
            return False
        self.ticker_cache[ticker] = current_time
        return True
    async def send_and_execute_webhook(self, hook: AsyncDiscordWebhook, embed: DiscordEmbed):
        hook.add_embed(embed)
        await hook.execute()

    async def create_channel_if_not_exists(self, ticker, name):
        # Check if the channel already exists
        if ticker not in self.created_channels:
            # If not, create the channel and add its name to the set
            await self.discord.create_channel(name=ticker, channel_description=name)
            self.created_channels.add(ticker)



    async def stock_rsi(self, ticker):
  


        time_day = 'day'
        time_hour = 'hour'
        time_minute = 'minute'
        time_week = 'week'
        time_month='month'
        rsi_min = asyncio.create_task(self.poly.rsi(ticker=ticker, timespan=time_minute))
        rsi_h = asyncio.create_task(self.poly.rsi(ticker=ticker, timespan=time_hour))
        rsi_d = asyncio.create_task(self.poly.rsi(ticker=ticker, timespan=time_day))
        rsi_w = asyncio.create_task(self.poly.rsi(ticker=ticker, timespan=time_week))
        rsi_mth = asyncio.create_task(self.poly.rsi(ticker=ticker, timespan=time_week))



        rsimin,rsihour,rsiday,rsiweek,rsimonth = await asyncio.gather(rsi_min, rsi_h, rsi_d, rsi_w,rsi_mth)
        rsimin = rsimin.rsi_value[0] if rsimin is not None and hasattr(rsimin, 'rsi_value') and isinstance(rsimin.rsi_value, list) and len(rsimin.rsi_value) > 0 else 0
        rsihour = rsihour.rsi_value[0] if rsihour is not None and hasattr(rsihour, 'rsi_value') and isinstance(rsihour.rsi_value, list) and len(rsihour.rsi_value) > 0 else 0
        rsiday = rsiday.rsi_value[0] if rsiday is not None and hasattr(rsiday, 'rsi_value') and isinstance(rsiday.rsi_value, list) and len(rsiday.rsi_value) > 0 else 0
        rsiweek = rsiweek.rsi_value[0] if rsiweek is not None and hasattr(rsiweek, 'rsi_value') and isinstance(rsiweek.rsi_value, list) and len(rsiweek.rsi_value) > 0 else 0
        rsimonth = rsimonth.rsi_value[0] if rsimonth is not None and hasattr(rsimonth, 'rsi_value')and isinstance(rsimonth.rsi_value, list) and len(rsimonth.rsi_value) > 0 else 0




        df = pd.DataFrame()
        if any(value >= 70 for value in (rsimin, rsihour, rsiday, rsiweek)):
            status = 'overbought'
            color = hex_color_dict['red']
            df['status'] =status
            df['color'] = color
            if time_minute:
                df['rsi'] = rsimin
                df['timespan'] = 'minute'

                rsiminhook = AsyncDiscordWebhook(os.environ.get('osob_minute'), content=f"<@375862240601047070>")
                embed = DiscordEmbed(title=f"Overbought RSI - {ticker} | MINUTE", description=f"```py\n{ticker} is currently trading {status} on the MINUTE timeframe with an RSI of {round(float(rsimin),2)}```", color=color)
                embed.set_timestamp()
                embed.set_footer(icon_url=os.environ.get('fudstop_logo'), text='Data by Polygon.io | Implemented by FUDSTOP')
                rsiminhook.add_embed(embed)
                await rsiminhook.execute()

                asyncio.create_task(self.db.batch_insert_dataframe(df, 'rsi_status', unique_columns='ticker, rsi, timespan'))

            if time_hour:
                df['rsi'] = rsihour
                df['timespan'] = 'hour'
                rsihourhook = AsyncDiscordWebhook(os.environ.get('osob_hour'), content=f"<@375862240601047070>")
                embed = DiscordEmbed(title=f"Overbought RSI - {ticker} | HOUR", description=f"```py\n{ticker} is currently trading {status} on the HOUR timeframe with an RSI of {round(float(rsimin),2)}```", color=color)
                embed.set_timestamp()
                embed.set_footer(icon_url=os.environ.get('fudstop_logo'), text='Data by Polygon.io | Implemented by FUDSTOP')
                rsihourhook.add_embed(embed)
                await rsihourhook.execute()

                asyncio.create_task(self.db.batch_insert_dataframe(df, 'rsi_status', unique_columns='ticker, rsi, timespan'))


            if time_day:
                df['rsi'] = rsiday
                df['timespan'] = 'day'
                df['ticker'] = ticker
                
                rsidayhook = AsyncDiscordWebhook(os.environ.get('osob_day'), content=f"<@375862240601047070>")
                embed = DiscordEmbed(title=f"Overbought RSI - {ticker} | DAY", description=f"```py\n{ticker} is currently trading {status} on the DAY timeframe with an RSI of {round(float(rsiday),2)}```", color=color)
                embed.set_timestamp()
                embed.set_footer(icon_url=os.environ.get('fudstop_logo'), text='Data by Polygon.io | Implemented by FUDSTOP')
                
                rsidayhook.add_embed(embed)
                await rsidayhook.execute()

                asyncio.create_task(self.db.batch_insert_dataframe(df, 'rsi_status', unique_columns='ticker, rsi, timespan'))

            if time_week:
        
                df['rsi'] = rsiweek
                df['timespan'] = 'week'
                weekhook = AsyncDiscordWebhook(os.environ.get('osob_week'), content=f"<@375862240601047070>")
                embed = DiscordEmbed(title=f"Overbought RSI - {ticker} | WEEK", description=f"```py\n{ticker} is currently trading {status} on the WEEK timeframe with an RSI of {round(float(rsiday),2)}```", color=color)
                embed.set_timestamp()
                embed.set_footer(icon_url=os.environ.get('fudstop_logo'), text='Data by Polygon.io | Implemented by FUDSTOP')
                
                weekhook.add_embed(embed)
                await weekhook.execute()

                asyncio.create_task(self.db.batch_insert_dataframe(df, 'rsi_status', unique_columns='ticker, rsi, timespan'))

            if time_month:
                df['rsi'] = rsimonth
                df['timespan'] = 'month'
            
                monthhook = AsyncDiscordWebhook(os.environ.get('osob_mth'), content=f"<@375862240601047070>")
                embed = DiscordEmbed(title=f"Overbought RSI - {ticker} | MONTH", description=f"```py\n{ticker} is currently trading {status} on the MONTH timeframe with an RSI of {round(float(rsiday),2)}```", color=color)
                embed.set_timestamp()
                embed.set_footer(icon_url=os.environ.get('fudstop_logo'), text='Data by Polygon.io | Implemented by FUDSTOP')
                
                monthhook.add_embed(embed)
                await monthhook.execute()

                asyncio.create_task(self.db.batch_insert_dataframe(df, 'rsi_status', unique_columns='ticker, rsi, timespan'))

        if any(value <= 30 for value in (rsimin, rsihour, rsiday, rsiweek)):

            status = 'oversold'
            color = hex_color_dict['green']
            df['status'] = status
            df['color'] = color
            if time_minute:
                df['rsi'] = rsimin
                df['timespan'] = 'minute'
                
                rsiminhook = AsyncDiscordWebhook(os.environ.get('osob_minute'), content=f"<@375862240601047070>")
                embed = DiscordEmbed(title=f"Oversold RSI - {ticker} | MINUTE", description=f"```py\n{ticker} is currently trading {status} on the MINUTE timeframe with an RSI of {round(float(rsimin),2)}```", color=color)
                embed.set_timestamp()
                embed.set_footer(icon_url=os.environ.get('fudstop_logo'), text='Data by Polygon.io | Implemented by FUDSTOP')
                
                rsiminhook.add_embed(embed)
                await rsiminhook.execute()
   
                asyncio.create_task(self.db.batch_insert_dataframe(df, 'rsi_status', unique_columns='ticker, rsi, timespan'))

            if time_day:
                df['rsi'] = rsiday
                df['timespan'] = 'day'
                
                rsidayhook = AsyncDiscordWebhook(os.environ.get('osob_day'), content=f"<@375862240601047070>")
                embed = DiscordEmbed(title=f"Oversold RSI - {ticker} | DAY", description=f"```py\n{ticker} is currently trading {status} on the DAY timeframe with an RSI of {round(float(rsiday),2)}```", color=color)
                embed.set_timestamp()
                embed.set_footer(icon_url=os.environ.get('fudstop_logo'), text='Data by Polygon.io | Implemented by FUDSTOP')
                
                rsidayhook.add_embed(embed)
                await rsidayhook.execute()
        
                asyncio.create_task(self.db.batch_insert_dataframe(df, 'rsi_status', unique_columns='ticker, rsi, timespan'))

            if time_hour:
        
                df['rsi'] = rsihour
                df['timespan'] = 'hour'    
                rsihourhook = AsyncDiscordWebhook(os.environ.get('osob_hour'), content=f"<@375862240601047070>")
                embed = DiscordEmbed(title=f"Oversold RSI - {ticker} | HOUR", description=f"```py\n{ticker} is currently trading {status} on the HOUR timeframe with an RSI of {round(float(rsiday),2)}```", color=color)
                embed.set_timestamp()
                embed.set_footer(icon_url=os.environ.get('fudstop_logo'), text='Data by Polygon.io | Implemented by FUDSTOP')
                
                rsihourhook.add_embed(embed)
                await rsihourhook.execute()
          
                asyncio.create_task(self.db.batch_insert_dataframe(df, 'rsi_status', unique_columns='ticker, rsi, timespan'))


            if time_week:
                df['rsi'] = rsiweek
                df['timespan'] = 'week'      
            
                weekhook = AsyncDiscordWebhook(os.environ.get('osob_week'), content=f"<@375862240601047070>")
                embed = DiscordEmbed(title=f"Oversold RSI - {ticker} | WEEK", description=f"```py\n{ticker} is currently trading {status} on the WEEK timeframe with an RSI of {round(float(rsiday),2)}```", color=color)
                embed.set_timestamp()
                embed.set_footer(icon_url=os.environ.get('fudstop_logo'), text='Data by Polygon.io | Implemented by FUDSTOP')
                
                weekhook.add_embed(embed)
                await weekhook.execute()
       
                asyncio.create_task(self.db.batch_insert_dataframe(df, 'rsi_status', unique_columns='ticker, rsi, timespan'))

            if time_month:
                df['rsi'] = rsimonth
                df['timespan'] = 'month'
                monthhook = AsyncDiscordWebhook(os.environ.get('osob_mth'), content=f"<@375862240601047070>")
                embed = DiscordEmbed(title=f"Oversold RSI - {ticker} | MONTH", description=f"```py\n{ticker} is currently trading {status} on the MONTH timeframe with an RSI of {round(float(rsiday),2)}```", color=color)
                embed.set_timestamp()
                embed.set_footer(icon_url=os.environ.get('fudstop_logo'), text='Data by Polygon.io | Implemented by FUDSTOP')
                
                monthhook.add_embed(embed)
                await monthhook.execute()

                asyncio.create_task(self.db.batch_insert_dataframe(df, 'rsi_status', unique_columns='ticker, rsi, timespan'))



    async def stock_macd(self, ticker):
        
       macd_m= asyncio.create_task(self.technicals.run_technical_scanner(ticker, self.time_minute))
       macd_d= asyncio.create_task(self.technicals.run_technical_scanner(ticker, self.time_day))
       macd_h= asyncio.create_task(self.technicals.run_technical_scanner(ticker, self.time_hour))
       macd_w= asyncio.create_task(self.technicals.run_technical_scanner(ticker, self.time_week))
       macd_mth= asyncio.create_task(self.technicals.run_technical_scanner(ticker, self.time_month))
    

       await asyncio.gather(macd_m, macd_d, macd_h, macd_w, macd_mth)



    async def crypto_conditions(self, dollar_cost, symbol, exchange, conditions, timestamp, size, price, color):


        if symbol in CRYPTO_HOOKS and dollar_cost >= 100:
            hook = CRYPTO_HOOKS[symbol]
            desc = CRYPTO_DESCRIPTIONS[symbol]

            
            webhook = AsyncDiscordWebhook(hook, content="<@375862240601047070>")
            embed = DiscordEmbed(title=f"{symbol} | Live Trades", description=f"```py\n{desc}```", color=hex_color_dict[color])
            embed.add_embed_field(name=f"Exchange:", value=f"> **{exchange}**")
            embed.add_embed_field(name=f"Side:", value=f"> **{conditions}**")
            embed.add_embed_field(name="Trade Info:", value=f"> Price: **${price}**\n> Size: **{size}**")
            embed.add_embed_field(name=f"Time:", value=f"> **{timestamp}**")
            embed.add_embed_field(name=f'Dollar Cost', value=f"# > **{dollar_cost}**")
            embed.set_footer(text=f"{symbol} | {conditions} | {dollar_cost} | {timestamp} | 10k+ cost | Data by polygon.io", icon_url=os.environ.get('fudstop_logo'))
            embed.set_timestamp()

            webhook.add_embed(embed)

            await webhook.execute()


        if symbol in CRYPTO_HOOKS and dollar_cost is not None and dollar_cost >= 10000 and conditions == 'Buy Side':
            hook = os.environ.get('crypto_10k_buys')
            desc = CRYPTO_DESCRIPTIONS[symbol]
            data_dict = { 
                'type': '10k buys',
                'dollar_cost': dollar_cost,
                'ticker': symbol,
                'description': desc,
                'exchange': exchange,
                'conditions': conditions,
                'timestamp': timestamp,
                'size': size,
                'price': price,
                'color': color
            }
            webhook = AsyncDiscordWebhook(hook, content="<@375862240601047070>")
            embed = DiscordEmbed(title=f"{symbol} | Live Trades", description=f"```py\n{desc}```", color=hex_color_dict['green'])
            embed.add_embed_field(name=f"Exchange:", value=f"> **{exchange}**")
            embed.add_embed_field(name=f"Side:", value=f"> **{conditions}**")
            embed.add_embed_field(name="Trade Info:", value=f"> Price: **${price}**\n> Size: **{size}**")
            embed.add_embed_field(name=f"Time:", value=f"> **{timestamp}**")
            embed.add_embed_field(name=f"Dollar Cost:", value=f"> **${dollar_cost}**")

            embed.set_footer(text=f"{symbol} | {conditions} | {round(float(dollar_cost),2)} | {timestamp} | 10k+ cost | Data by polygon.io", icon_url=os.environ.get('fudstop_logo'))
            embed.set_timestamp()

            webhook.add_embed(embed)
            await webhook.execute()
            asyncio.create_task(self.db.batch_insert_dataframe(df, table_name='large_crypto', unique_columns='insertion_timestamp'))

        if symbol in CRYPTO_HOOKS and dollar_cost is not None and dollar_cost >= 10000 and conditions == 'Sell Side':
            hook=os.environ.get('crypto_10k_sells')
     
            desc = CRYPTO_DESCRIPTIONS[symbol]
            data_dict = { 
                'type': '10k sells',
                'dollar_cost': dollar_cost,
                'ticker': symbol,
                'description': desc,
                'exchange': exchange,
                'conditions': conditions,
                'timestamp': timestamp,
                'size': size,
                'price': price,
                'color': color
            }
            webhook = AsyncDiscordWebhook(hook, content="<@375862240601047070>")
            embed = DiscordEmbed(title=f"{symbol} | Live Trades", description=f"```py\n{desc}```", color=hex_color_dict['red'])
            embed.add_embed_field(name=f"Exchange:", value=f"> **{exchange}**")
            embed.add_embed_field(name=f"Side:", value=f"> **{conditions}**")
            embed.add_embed_field(name="Trade Info:", value=f"> Price: **${price}**\n> Size: **{size}**")
            embed.add_embed_field(name=f"Time:", value=f"> **{timestamp}**")
            embed.add_embed_field(name=f"Dollar Cost:", value=f"> **${dollar_cost}**")

            embed.set_footer(text=f"{symbol} | {conditions} | {round(float(dollar_cost),2)} | {timestamp} | 10k+ cost | Data by polygon.io", icon_url=os.environ.get('fudstop_logo'))
            embed.set_timestamp()

            webhook.add_embed(embed)

            await webhook.execute()

            df = pd.DataFrame(data_dict)
            asyncio.create_task(self.db.batch_insert_dataframe(df, table_name='large_crypto', unique_columns='insertion_timestamp'))


    
    async def process_batches(self, tickers_string: asyncio.Queue):
        


        data= await self.opts.multi_snapshot(tickers_string)




        df = data.as_dataframe.rename(columns={'intrinstic_value': 'intrinsic_value'})
        

        await self.db.batch_insert_dataframe(data.as_dataframe, table_name='poly_opts', unique_columns='insertion_timestamp', batch_size=250)

        df = data.as_dataframe
        yield df




    # Function to handle incoming WebSocket messages
            
    async def handle_msg(self, msgs: WebSocketMessage):

  
        monitor = EquityOptionTradeMonitor()
        
        for m in msgs:
         
            event_type = m.event_type



            if event_type == 'A' and m.symbol.startswith('O:'):
                async for data in self.db.insert_option_aggs(m):
                    ticker = data.get('option_symbol')
                    symbol = data.get('ticker')
                    self.agg_tickers.append(m.symbol)  # Append to the instance's deque

                    # When we have 250 tickers, process them
                    if len(self.agg_tickers) == 250:
                        tickers_string = ','.join(self.agg_tickers)
                        # Process the tickers_string as needed
                    


                        async for df in self.process_batches(tickers_string):
                            processed_data = set()  # Initialize a set to store processed data points
                            
                            for i,row in df.head(5).iterrows():
                                data_identifier = f"{row['ticker']}_{row['timestamp']}"

                                # Check if the data point has already been processed
                                if data_identifier in processed_data:
                                    continue  # Skip processing if it's a duplicate
                                else:
                                    processed_data.add(data_identifier)
                                # Access each column value from the row
                                oi_value = row['oi']
                                vol_value = row['vol']
                                vol_oi_value = row['vol_oi_ratio']
                                iv_value = row['iv']
                                ask_value = row['ask']
                                bid_value = row['bid']
                                mid_value = row['mid']
                                strike_value = row['strike']
                                expiry_value = row['expiry']
                                call_put_value = row['cp']
                                underlying_symbol_value = row['ticker']
                                underlying_price_value = row['underlying_price']
                                gamma_value = row['gamma']
                                gamma_risk_value = row['gamma_risk']
                                delta_value = row['delta']
                                delta_theta_value = row['delta_theta_ratio']
                                theta_value = row['theta']
                                theta_decay_value = row['theta_decay_rate']
                                vega_value = row['vega']
                                vega_impact_value = row['vega_impact']
                                change_percent_value = row['change_percent']
                                close_value = row['close']
                                open_value = row['open']
                                high_value = row['high']
                                low_value = row['low']
                                vwap_value = row['vwap']

                                ex_value_value = row['extrinsic_value']
                                in_value_value = row['intrinsic_value']
                                iv_percentile_value = row['iv_percentile']
                                moneyness_value = row['moneyness']
                                velocity_value = row['velocity']
                                profit_potential_value = row['opp']
                                spread_value = row['spread']
                                spread_pct_value = row['spread_pct']
                                time_value_value = row['time_value']
                                trade_size_value = row['trade_size']
                                trade_price_value = row['price']
                                trade_exchange_value = row['exchange']
                                
                                if call_put_value == 'call':
                                    color = hex_color_dict['green']
                                else:
                                    color = hex_color_dict['red']
                              

                                
                                if oi_value >= 100000:
                                    hook = AsyncDiscordWebhook(os.environ.get('oi_100kplus'))
                    

                                    embed = DiscordEmbed(title=f"{underlying_symbol_value} | ${underlying_price_value} | {strike_value} | {expiry_value}", description=f"```py\nThese contracts are trading with OI values greater than 100,000 contracts.```", color=color)
                                    embed.add_embed_field(name=f"Contract Stats:", value=f"> OPEN: **${open_value}**\n> HIGH: **${high_value}**\n> LOW: **${low_value}**\n> CLOSE: **${close_value}**\n> VWAP: **${vwap_value}**\n> CHANGE%: **{change_percent_value}**")
                                    embed.add_embed_field(name=f"OI / VOl", value=f"> OI: **{oi_value}**\n> VOL: **{vol_value}**\n> RATIO: **{vol_oi_value}**")
                                    embed.add_embed_field(name=f"IV:", value=f"> **{iv_value}**\n> Percentile: **{iv_percentile_value}**")
                                    embed.add_embed_field(name=f"Value:", value=f"> Intrinsic: **{in_value_value}**\n> Extrinsic: **{ex_value_value}**\n> Time: **{time_value_value}**")
                                    embed.add_embed_field(name=f"Spread:", value=f"> Bid: **${bid_value}**\n> Mid: **${mid_value}**\n> Ask: **{ask_value}**\n> Spread: **{round(float(spread_value),2)}**\n> Spread PCT: **{spread_pct_value}%**")
                                    embed.add_embed_field(name=f"Last Trade", value=f"> Size: **{trade_size_value}**\n> Price: **{trade_price_value}**\n> Exchange: **{trade_exchange_value}**")
                                    embed.add_embed_field(name="Details:", value=f"> Moneyness: **{moneyness_value}**\n> Velocity: **{velocity_value}**\n> Profit Potential: **{profit_potential_value}**")
                                    embed.add_embed_field(name=f"GREEKS:", value=f"> Delta: **{delta_value}**\n> Delta/Theta Ratio: **{delta_theta_value}**\n> Gamma: **{gamma_value}**\n> Gamma Risk: **{gamma_risk_value}**\n> Vega: **{vega_value}**\n> Vega Impact: **{vega_impact_value}**\n> Theta: **{theta_value}**\n> Decay Rate: **{theta_decay_value}**", inline=False)
                                    embed.set_timestamp()
                                    embed.set_footer(text='OI 100k+ | Data by Polygon.io | Implemented by FUDSTOP')
                                    asyncio.create_task(self.analyzer.send_hook(hook, embed))
                                    asyncio.create_task(asyncio.sleep(1))
                                if oi_value >= 1000 and oi_value <= 4999:
                                    hook = AsyncDiscordWebhook(os.environ.get('oi_5k10k'))

                                    embed = DiscordEmbed(title=f"{underlying_symbol_value} | ${underlying_price_value} | {strike_value} | {expiry_value}", description=f"```py\nThese contracts are trading with OI values between 1000 and 5000.```", color=color)
                                    embed.add_embed_field(name=f"Contract Stats:", value=f"> OPEN: **${open_value}**\n> HIGH: **${high_value}**\n> LOW: **${low_value}**\n> CLOSE: **${close_value}**\n> VWAP: **${vwap_value}**\n> CHANGE%: **{change_percent_value}**")
                                    embed.add_embed_field(name=f"OI / VOl", value=f"> OI: **{oi_value}**\n> VOL: **{vol_value}**\n> RATIO: **{vol_oi_value}**")
                                    embed.add_embed_field(name=f"Value:", value=f"> Intrinsic: **{in_value_value}**\n> Extrinsic: **{ex_value_value}**\n> Time: **{time_value_value}**")
                                    embed.add_embed_field(name=f"Spread:", value=f"> Bid: **${bid_value}**\n> Mid: **${mid_value}**\n> Ask: **{ask_value}**\n> Spread: **{round(float(spread_value),2)}**\n> Spread PCT: **{spread_pct_value}%**")
                                    embed.add_embed_field(name=f"Last Trade", value=f"> Size: **{trade_size_value}**\n> Price: **{trade_price_value}**\n> Exchange: **{trade_exchange_value}**")
                                    embed.add_embed_field(name="Details:", value=f"> Moneyness: **{moneyness_value}**\n> Velocity: **{velocity_value}**\n> Profit Potential: **{profit_potential_value}**")
                                    embed.add_embed_field(name=f"GREEKS:", value=f"> Delta: **{delta_value}**\n> Delta/Theta Ratio: **{delta_theta_value}**\n> Gamma: **{gamma_value}**\n> Gamma Risk: **{gamma_risk_value}**\n> Vega: **{vega_value}**\n> Vega Impact: **{vega_impact_value}**\n> Theta: **{theta_value}**\n> Decay Rate: **{theta_decay_value}**", inline=False)

                                    embed.set_timestamp()
                                    embed.set_footer(text='OI 1k to 5k | Data by Polygon.io | Implemented by FUDSTOP')
                                    asyncio.create_task(self.analyzer.send_hook(hook, embed))
                                    asyncio.create_task(asyncio.sleep(1))


                                if oi_value >= 10000 and oi_value <= 49999:
                                    hook = AsyncDiscordWebhook(os.environ.get('oi_10k50k'))

                                    embed = DiscordEmbed(title=f"{underlying_symbol_value} | ${underlying_price_value} | {strike_value} | {expiry_value}", description=f"```py\nThese contracts are trading with OI values between 10,000 and 50,000 contracts.```", color=color)
                                    embed.add_embed_field(name=f"Contract Stats:", value=f"> OPEN: **${open_value}**\n> HIGH: **${high_value}**\n> LOW: **${low_value}**\n> CLOSE: **${close_value}**\n> VWAP: **${vwap_value}**\n> CHANGE%: **{change_percent_value}**")
                                    embed.add_embed_field(name=f"OI / VOl", value=f"> OI: **{oi_value}**\n> VOL: **{vol_value}**\n> RATIO: **{vol_oi_value}**")
                                    embed.add_embed_field(name=f"IV:", value=f"> **{iv_value}**\n> Percentile: **{iv_percentile_value}**")
                                    embed.add_embed_field(name=f"Value:", value=f"> Intrinsic: **{in_value_value}**\n> Extrinsic: **{ex_value_value}**\n> Time: **{time_value_value}**")
                                    embed.add_embed_field(name=f"Spread:", value=f"> Bid: **${bid_value}**\n> Mid: **${mid_value}**\n> Ask: **{ask_value}**\n> Spread: **{round(float(spread_value),2)}**\n> Spread PCT: **{spread_pct_value}%**")
                                    embed.add_embed_field(name=f"Last Trade", value=f"> Size: **{trade_size_value}**\n> Price: **{trade_price_value}**\n> Exchange: **{trade_exchange_value}**")
                                    embed.add_embed_field(name="Details:", value=f"> Moneyness: **{moneyness_value}**\n> Velocity: **{velocity_value}**\n> Profit Potential: **{profit_potential_value}**")
                                    embed.add_embed_field(name=f"GREEKS:", value=f"> Delta: **{delta_value}**\n> Delta/Theta Ratio: **{delta_theta_value}**\n> Gamma: **{gamma_value}**\n> Gamma Risk: **{gamma_risk_value}**\n> Vega: **{vega_value}**\n> Vega Impact: **{vega_impact_value}**\n> Theta: **{theta_value}**\n> Decay Rate: **{theta_decay_value}**", inline=False)

                                    embed.set_timestamp()
                                    embed.set_footer(text='OI 10k to 50k | Data by Polygon.io | Implemented by FUDSTOP')
                                    asyncio.create_task(self.analyzer.send_hook(hook, embed))
                                    asyncio.create_task(asyncio.sleep(1))



                                if oi_value >= 50000 and oi_value <= 99999:
                                    hook = AsyncDiscordWebhook(os.environ.get('oi_50k100k'))

                                    embed = DiscordEmbed(title=f"{underlying_symbol_value} | ${underlying_price_value} | {strike_value} | {expiry_value}", description=f"```py\nThese contracts are trading with OI values between 50,000 and 100,000 contracts.```", color=color)
                                    embed.add_embed_field(name=f"Contract Stats:", value=f"> OPEN: **${open_value}**\n> HIGH: **${high_value}**\n> LOW: **${low_value}**\n> CLOSE: **${close_value}**\n> VWAP: **${vwap_value}**\n> CHANGE%: **{change_percent_value}**")
                                    embed.add_embed_field(name=f"OI / VOl", value=f"> OI: **{oi_value}**\n> VOL: **{vol_value}**\n> RATIO: **{vol_oi_value}**")
                                    embed.add_embed_field(name=f"IV:", value=f"> **{iv_value}**\n> Percentile: **{iv_percentile_value}**")
                                    embed.add_embed_field(name=f"Value:", value=f"> Intrinsic: **{in_value_value}**\n> Extrinsic: **{ex_value_value}**\n> Time: **{time_value_value}**")
                                    embed.add_embed_field(name=f"Spread:", value=f"> Bid: **${bid_value}**\n> Mid: **${mid_value}**\n> Ask: **{ask_value}**\n> Spread: **{round(float(spread_value),2)}**\n> Spread PCT: **{spread_pct_value}%**")
                                    embed.add_embed_field(name=f"Last Trade", value=f"> Size: **{trade_size_value}**\n> Price: **{trade_price_value}**\n> Exchange: **{trade_exchange_value}**")
                                    embed.add_embed_field(name="Details:", value=f"> Moneyness: **{moneyness_value}**\n> Velocity: **{velocity_value}**\n> Profit Potential: **{profit_potential_value}**")
                                    embed.add_embed_field(name=f"GREEKS:", value=f"> Delta: **{delta_value}**\n> Delta/Theta Ratio: **{delta_theta_value}**\n> Gamma: **{gamma_value}**\n> Gamma Risk: **{gamma_risk_value}**\n> Vega: **{vega_value}**\n> Vega Impact: **{vega_impact_value}**\n> Theta: **{theta_value}**\n> Decay Rate: **{theta_decay_value}**", inline=False)
                                    embed.set_timestamp()
                                    embed.set_footer(text='OI 50k to 100k | Data by Polygon.io | Implemented by FUDSTOP')
                                    asyncio.create_task(self.analyzer.send_hook(hook, embed))
                                    asyncio.create_task(asyncio.sleep(1))


                                if theta_value <= -0.01 and theta_value >= -0.03 and ask_value >= 0.18 and ask_value <= 1.50:
                                    hook = AsyncDiscordWebhook(os.environ.get('theta_resistant'))
                                    embed = DiscordEmbed(title=f"Theta RESISTANT | {underlying_symbol_value} | ${strike_value} | {call_put_value} | {expiry_value}", description=f"```py\nThese contracts have high theta values - meaning they lose value to time decay SLOWER. Good for long-term horizons / hedging.```",color=color)
                                    embed.add_embed_field(name=f"Contract Stats:", value=f"> OPEN: **${open_value}**\n> HIGH: **${high_value}**\n> LOW: **${low_value}**\n> CLOSE: **${close_value}**\n> VWAP: **${vwap_value}**\n> CHANGE%: **{change_percent_value}**")
                                    embed.add_embed_field(name=f"OI / VOl", value=f"> OI: **{oi_value}**\n> VOL: **{vol_value}**\n> RATIO: **{vol_oi_value}**")
                                    embed.add_embed_field(name=f"IV:", value=f"> **{iv_value}**\n> Percentile: **{iv_percentile_value}**")
                                    embed.add_embed_field(name=f"Value:", value=f"> Intrinsic: **{in_value_value}**\n> Extrinsic: **{ex_value_value}**\n> Time: **{time_value_value}**")
                                    embed.add_embed_field(name=f"Spread:", value=f"> Bid: **${bid_value}**\n> Mid: **${mid_value}**\n> Ask: **{ask_value}**\n> Spread: **{round(float(spread_value),2)}**\n> Spread PCT: **{spread_pct_value}%**")
                                    embed.add_embed_field(name=f"Last Trade", value=f"> Size: **{trade_size_value}**\n> Price: **{trade_price_value}**\n> Exchange: **{trade_exchange_value}**")
                                    embed.add_embed_field(name="Details:", value=f"> Moneyness: **{moneyness_value}**\n> Velocity: **{velocity_value}**\n> Profit Potential: **{profit_potential_value}**")
                                    embed.add_embed_field(name=f"GREEKS:", value=f"> Delta: **{delta_value}**\n> Delta/Theta Ratio: **{delta_theta_value}**\n> Gamma: **{gamma_value}**\n> Gamma Risk: **{gamma_risk_value}**\n> Vega: **{vega_value}**\n> Vega Impact: **{vega_impact_value}**\n> Theta: **{theta_value}**\n> Decay Rate: **{theta_decay_value}**", inline=False)
                                    embed.set_timestamp()
                                    embed.set_footer(text='Theta Resistant | Data by Polygon.io | Implemented by FUDSTOP')




                                    asyncio.create_task(self.analyzer.send_hook(hook, embed))
                                    asyncio.create_task(asyncio.sleep(1))






                                asyncio.create_task(asyncio.sleep(1))

                                

            #stock aggs
            elif event_type == 'A' and not m.symbol.startswith('I:') and not m.symbol.startswith("O:"):
                if m.symbol in set(most_active_tickers):
                    async for data in self.db.insert_stock_aggs(m):
                        ticker = data.get('ticker')
                        
                        await self.queue.put(data)

                        asyncio.create_task(self.stock_rsi(ticker))
                        asyncio.create_task(self.stock_macd(ticker))


            #option trades
            
            elif event_type == 'T' and m.symbol.startswith('O:'):
                
                async for data in self.db.insert_option_trades(m):
                    size = data.get('size')
                    symbol = data.get('ticker')
                
                    ticker = data.get('option_symbol')
                    
                    dollar_cost = data.get('dollar_cost')
                    expiry = data.get('expiry')
                    strike = data.get('strike')
                    call_put = data.get('call_put')
                    hour_of_day = data.get('hour_of_day')
                    weekday = data.get('weekday')
                    conditions = data.get('conditions')
                    price = data.get('price')
                    volume_change = data.get('volume_change')
                    price_change = data.get('price_change')
                    exchange = data.get('exchange')
                    self.trade_tickers.append(ticker)
                

                    if data.get('size') is not None and data.get('size') >= 500 and data.get('conditions') in option_conditions_hooks:
                        hook = option_conditions_hooks[data.get('conditions')]
                        asyncio.create_task(option_condition_embed(price_to_strike=data.get('price_to_strike'),conditions=data.get('conditions'), option_symbol=ticker,underlying_symbol=symbol,strike=data.get('strike'),call_put=data.get('call_put'),expiry=data.get('expiry'),price = data.get('price'), size=data.get('size'),exchange = data.get('exchange'),volume_change = data.get('volume_change'),price_change=data.get('price_change'),weekday=data.get('weekday'),hour_of_day=data.get('hour_of_day'), hook=hook))


    


                    if size is not None and size >= 10000 and size <= 49999:
                        asyncio.create_task(sized_trade_embed(dollar_cost=dollar_cost,expiry=expiry,option_symbol=ticker,call_put=call_put,strike=strike,underlying_symbol=symbol,price=price,price_change=price_change,size=size,volume_change=volume_change,conditions=conditions,exchange=exchange,price_to_strike=data.get('price_to_strike'),hour_of_day=hour_of_day,weekday=weekday))

                    if size is not None and size >= 50000:
                        asyncio.create_task(sized_trade_embed(dollar_cost=dollar_cost,expiry=expiry,option_symbol=ticker,call_put=call_put,strike=strike,underlying_symbol=symbol,price=price,price_change=price_change,size=size,volume_change=volume_change,conditions=conditions,exchange=exchange,price_to_strike=data.get('price_to_strike'),hour_of_day=hour_of_day,weekday=weekday))



            #stock trades
            elif event_type == 'T' and not m.symbol.startswith('O:') and not m.symbol.startswith('I:'):
                async for data in self.db.insert_stock_trades(m):
                
                    await self.queue.put(data)

                    ticker = data.get('ticker')
                    if ticker in set(most_active_tickers):
        
                        # Call the repeated_hits method
                        last_five_trades = await monitor.repeated_hits(data)
                        embed = DiscordEmbed(title='Repeated Stock Hits', description=f"# > {ticker}", color=hex_color_dict['gold'])
                        
                        if last_five_trades:
                            # Do something with the last five trades

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
                            
                    
                            hook = AsyncDiscordWebhook(os.environ.get('repeated_hits'))
                            embed.set_timestamp()

                            asyncio.create_task(self.send_and_execute_webhook(hook, embed))


                    





            elif event_type == 'XT':
                async for data in self.db.insert_crypto_trades(m):
                    ticker = data.get('ticker')
                    print(f"CRYPTO TRADES: {ticker}")
                    # Call the repeated_hits method
                    last_five_trades = await monitor.repeated_hits(data)

                    # Check if the ticker has appeared 5 times in a row
                    if last_five_trades == 5:
                        embed = DiscordEmbed(title='Repeated Stock Hits', description=f"# > {ticker}")
                        print(f"{ticker} has appeared 5 times in a row.")
                        hook = AsyncDiscordWebhook(os.environ.get('repeated_hits'))
                        hook.add_embed(embed)
                        await hook.execute()


                    asyncio.create_task(self.crypto_conditions(data.get('dollar_cost'), data.get('ticker'), data.get('exchange'), data.get('conditions'), data.get('timestamp'),data.get('size'), data.get('price'),data.get('color')))
                    

            elif event_type == 'CAS':
                async for data in self.db.insert_forex_aggs(m=m):
                    ticker = data.get('ticker')
                    print(f"FOREX AGGS: {ticker}")


    async def insert_new_prices(self, ticker, type, fifty_high, price, fifty_low, timestamp):
        try:

    

            # Insert data into the market_data table
            await self.conn.execute('''
                INSERT INTO new_prices(ticker, type, fifty_high, price, fifty_low, timestamp)
                VALUES($1, $2, $3, $4, $5, $6)
                ''', ticker, type, fifty_high, price, fifty_low, timestamp)
            

        except UniqueViolationError:
            pass





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
            client = WebSocketClient(subscriptions=[pattern], api_key=os.environ.get('YOUR_POLYGON_KEY'), market=live_market, verbose=True)
            clients.append(client.connect(market.handle_msg))

    await asyncio.gather(*clients, return_exceptions=True)  # Wait for all clients to finish



asyncio.run(main())

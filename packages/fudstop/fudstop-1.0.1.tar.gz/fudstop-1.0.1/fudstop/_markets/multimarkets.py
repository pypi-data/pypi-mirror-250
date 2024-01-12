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
from dotenv import load_dotenv
from embeddings import vol_anal_embed, create_newhigh_embed, profit_ratio_02_embed, profit_ratio_98_embed
from fudstop._markets.list_sets.dicts import hex_color_dict
from apis.discord_.discord_sdk import DiscordSDK
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
from apis.polygonio.async_polygon_sdk import Polygon
class MultiMarkets:
    def __init__(self, user, database, port, host, password):
        self.poly = Polygon(host='localhost', user='chuck', database='markets', password='fud', port=5432)
        self.discord = DiscordSDK()
        self.technicals = Technicals()
        self.db = MarketDBManager(user=user,database=database,port=port,host=host,password=password)
        self.markets = [Market.Options, Market.Stocks, Market.Indices, Market.Forex, Market.Crypto]# Market.Forex, Market.Indices]
        self.subscription_patterns = {
            Market.Options: ["T.*,A.*"],
            Market.Stocks: ["A.*,T.*"],
            Market.Indices: ["A.*"],
            Market.Crypto: ['XT.*'],
            Market.Forex: ['CAS.*']

        }
        self.ticker_cache = {}
        self.trading = WebullTrading()
        self.time_day = 'day'
        self.time_hour = 'hour'
        self.time_minute = 'minute'
        self.time_week = 'week'
        self.time_month='month'
        self.queue = asyncio.Queue()
        self.created_channels = set()  # A set to keep track of created channels
        self.last_ticker = None
        self.consecutive_count = 0
        self.indices_names=indices_names_and_symbols_dict



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
        data = await self.queue.get()



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
        rsimin = rsimin.rsi_value[0] if rsimin is not None and hasattr(rsimin, 'rsi_value') and len(rsimin.rsi_value) > 0 else 0
        rsihour = rsihour.rsi_value[0] if rsihour is not None and hasattr(rsihour, 'rsi_value')and len(rsihour.rsi_value) > 0 else 0
        rsiday = rsiday.rsi_value[0] if rsiday is not None and hasattr(rsiday, 'rsi_value')and len(rsiday.rsi_value) > 0 else 0
        rsiweek = rsiweek.rsi_value[0] if rsiweek is not None and hasattr(rsiweek, 'rsi_value')and len(rsiweek.rsi_value) > 0 else 0
        rsimonth = rsimonth.rsi_value[0] if rsimonth is not None and hasattr(rsimonth, 'rsi_value')and len(rsimonth.rsi_value) > 0 else 0



        df = pd.DataFrame(data, index=[0])
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
            print(hook)
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


    async def stock_analysis(self, ticker):
        fire_sale = os.environ.get('fire_sale')
        neutral_zone = os.environ.get('neutral_zone')
        accumulation = os.environ.get('accumulation')
        cost_dist_98 = os.environ.get('cost_dist_98')
        cost_dist_02 = os.environ.get('cost_dist_02')
        new_high = os.environ.get('new_high')
        new_low = os.environ.get('new_low')
        near_52_high = os.environ.get('near_52_high')
        near_52_low = os.environ.get('near_52_low')
        below_avg_vol = os.environ.get('below_avg_vol')
        above_avg_vol = os.environ.get('above_avg_vol')
        quote_task = asyncio.create_task(self.trading.stock_quote(ticker))

        vol_task = asyncio.create_task(self.trading.volume_analysis(ticker))
        try:
            cost_dist_task = asyncio.create_task(self.trading.cost_distribution(ticker))
        except ContentTypeError:
            print('Content Error')

        result = await asyncio.gather(quote_task, vol_task, cost_dist_task)
        yield result[0], result[1], result[2]
        fifty_high = result[0].fifty_high
        fifty_low = result[0].fifty_low
        price = result[0].web_stock_close
        o = result[0].web_stock_open
        h = result[0].web_stock_high
        l = result[0].web_stock_low
        vol = result[0].web_stock_vol
        avg10d = result[0].avg_10d_vol
        avg3m = result[0].avg_vol3m

        r = result[0]
        vol_anal = result[1]
        buyPct = vol_anal.buyPct
        sellPct = vol_anal.sellPct
        neutPct = vol_anal.nPct
        avgPrice = vol_anal.avePrice


        cost_dist = result[2]
        # Check and call analyze_profit_ratio
        if cost_dist is not None and self.should_process_stock(ticker):
            asyncio.create_task(self.analyze_profit_ratio(cost_dist,cost_dist_98,cost_dist_02,ticker,price,hex_color_dict,o,h,l,vol,avg10d,avg3m,buyPct,neutPct,sellPct,fifty_high,fifty_low))

        # Check and call analyze_volume
        if avg3m is not None and avg10d is not None and vol is not None and self.should_process_stock(ticker):
            asyncio.create_task(self.analyze_volume(avg3m,avg10d,vol,r,ticker,hex_color_dict,below_avg_vol,above_avg_vol,buyPct,sellPct,neutPct,avgPrice,fifty_high,fifty_low,price))

        # Check and call analyze_stock_prices
        if fifty_high is not None and fifty_low is not None and self.should_process_stock(ticker):
            asyncio.create_task(self.analyze_stock_prices(fifty_high,fifty_low,price,r,ticker,hex_color_dict,near_52_high,near_52_low,new_high,new_low))

        # Check and call analyze_volume_distribution
        if buyPct is not None and sellPct is not None and neutPct is not None and self.should_process_stock(ticker):
            asyncio.create_task(self.analyze_volume_distribution(buyPct,sellPct,neutPct,r,ticker,hex_color_dict,fire_sale,accumulation,neutral_zone))


    async def insert_new_prices(self, ticker, type, fifty_high, price, fifty_low, timestamp, conn):
        try:

    

            # Insert data into the market_data table
            await conn.execute('''
                INSERT INTO new_prices(ticker, type, fifty_high, price, fifty_low, timestamp)
                VALUES($1, $2, $3, $4, $5, $6)
                ''', ticker, type, fifty_high, price, fifty_low, timestamp)
            

        except UniqueViolationError:
            pass


    async def analyze_volume_distribution(self, buyPct, sellPct, neutPct, r, ticker, hex_colors, fire_sale, accumulation, neutral_zone):
        try:
            if buyPct is not None and sellPct is not None and neutPct is not None:
                if sellPct >= 65:
                    color = hex_colors['red']
                    desc = f"```py\n{ticker} is currently under FIRE SALE status - as the recorded volume on the day is 65% or more SELL SIDE VOLUME.```"
                    await vol_anal_embed(webhook=fire_sale, symbol=ticker, o=r.web_stock_open, h=r.web_stock_high, l=r.web_stock_low, c=r.web_stock_close, cr=r.web_change_ratio, f2h=r.fifty_low, v=r.web_stock_vol, type='Fire Sale', color=color, description=desc, buyPct=buyPct, sellPct=sellPct, neutPct=neutPct)

                if buyPct >= 65:
                    desc = f"```py\n{ticker} is currently under ACCUMULATION status - as the recorded volume on the day is 65% or more BUY SIDE VOLUME.```"
                    color = hex_colors['green']
                    await vol_anal_embed(webhook=accumulation, symbol=ticker, o=r.web_stock_open, h=r.web_stock_high, l=r.web_stock_low, c=r.web_stock_close, cr=r.web_change_ratio, f2h=r.fifty_low, v=r.web_stock_vol, type='Accumulation', color=color, description=desc, buyPct=buyPct, sellPct=sellPct, neutPct=neutPct)

                if neutPct >= 65:
                    desc = f"```py\n{ticker} is currently under NEUTRAL ZONE status - as the recorded volume on the day is 65% or more NEUTRAL SIDE VOLUME.```"
                    color = hex_colors['gray']
                    await vol_anal_embed(webhook=neutral_zone, symbol=ticker, o=r.web_stock_open, h=r.web_stock_high, l=r.web_stock_low, c=r.web_stock_close, cr=r.web_change_ratio, f2h=r.fifty_low, v=r.web_stock_vol, type='Neutral Zone', color=color, description=desc, buyPct=buyPct, sellPct=sellPct, neutPct=neutPct)
            
        except Exception as e:
            # Handle or log the exception as needed
            print(f"An error occurred: {e}")
            return None

        return "Volume analysis completed"


    async def analyze_stock_prices(self, fifty_high, fifty_low, close, r, ticker, timestamp, hex_colors, near_52_high, near_52_low, new_high, new_low):
        try:
            if fifty_high is not None and fifty_low is not None:
                # New checks for near 52-week high/low
                high_margin = float(fifty_high) * 0.95
                low_margin = float(fifty_low) * 1.05
                if high_margin <= close <= float(fifty_high):
                    await create_newhigh_embed(webhook=near_52_high, symbol=r.web_symb, o=r.web_stock_open, h=r.web_stock_high, l=r.web_stock_low, c=r.web_stock_close, cr=r.web_change_ratio, f2l=r.fifty_low, av10d=r.avg_10d_vol, av3m=r.avg_vol3m, vr=r.web_vibrate_ratio, f2h=r.fifty_high, v=r.web_stock_vol, type='Near High!', color=hex_colors['red'])
                    asyncio.create_task(self.insert_new_prices(ticker=ticker, type='near high', fifty_high=r.fifty_high, price=r.web_stock_close, fifty_low=r.fifty_low, timestamp=timestamp))

                elif float(fifty_low) <= close <= low_margin:
                    await create_newhigh_embed(webhook=near_52_low, symbol=r.web_symb, o=r.web_stock_open, h=r.web_stock_high, l=r.web_stock_low, c=r.web_stock_close, cr=r.web_change_ratio, f2l=r.fifty_low, av10d=r.avg_10d_vol, av3m=r.avg_vol3m, vr=r.web_vibrate_ratio, f2h=r.fifty_high, v=r.web_stock_vol, type='Near Low!', color=hex_colors['green'])
                    asyncio.create_task(self.insert_new_prices(ticker=ticker, type='near low', fifty_high=r.fifty_high, price=r.web_stock_close, fifty_low=r.fifty_low, timestamp=timestamp))

                elif float(fifty_high) == close:
                    await create_newhigh_embed(webhook=new_high, symbol=r.web_symb, o=r.web_stock_open, h=r.web_stock_high, l=r.web_stock_low, c=r.web_stock_close, cr=r.web_change_ratio, f2l=r.fifty_low, av10d=r.avg_10d_vol, av3m=r.avg_vol3m, vr=r.web_vibrate_ratio, f2h=r.fifty_high, v=r.web_stock_vol, type='New High!', color=hex_colors['red'])
                    asyncio.create_task(self.insert_new_prices(ticker=ticker, type='new high', fifty_high=r.fifty_high, price=r.web_stock_close, fifty_low=r.fifty_low, timestamp=timestamp))

                elif float(fifty_low) == close:
                    await create_newhigh_embed(webhook=new_low, symbol=r.web_symb, o=r.web_stock_open, h=r.web_stock_high, l=r.web_stock_low, c=r.web_stock_close, cr=r.web_change_ratio, f2l=r.fifty_low, av10d=r.avg_10d_vol, av3m=r.avg_vol3m, vr=r.web_vibrate_ratio, f2h=r.fifty_high, v=r.web_stock_vol, type='New Low!', color=hex_colors['green'])
                    await self.insert_new_prices(ticker=ticker, type='new low', fifty_high=r.fifty_high, price=r.web_stock_close, fifty_low=r.fifty_low, timestamp=timestamp)
            
        except Exception as e:
            # Handle or log the exception as needed
            print(f"An error occurred: {e}")
            return None

        return "Analysis completed"



    async def analyze_profit_ratio(self, cost_dist, cost_dist_98, cost_dist_02, ticker, price, hex_colors, o, h, l, vol, avg10d, avg3m, buyPct, neutPct, sellPct, fifty_high, fifty_low):
        try:
            if cost_dist is not None:
                profit_ratio = round(float(cost_dist.closeProfitRatio) * 100, 2)

                if profit_ratio >= 98:
                    await profit_ratio_98_embed(profit_ratio, cost_dist_98, ticker, price, hex_colors, o, h, l, vol, avg10d, avg3m, buyPct, neutPct, sellPct, fifty_high, fifty_low)

                elif profit_ratio <= 2:
                    await profit_ratio_02_embed(profit_ratio, cost_dist_02, ticker, price, hex_colors, o, h, l, vol, avg10d, avg3m, buyPct, neutPct, sellPct, fifty_high, fifty_low)

        except Exception as e:
            # Handle or log the exception as needed
            print(f"An error occurred: {e}")
            return None

        return "Profit ratio analysis completed"


    async def analyze_volume(self, avg3m, avg10d, vol, r, ticker, hex_colors, below_avg_vol, above_avg_vol, buyPct, sellPct, neutPct, avgPrice, fifty_high, fifty_low, timestamp, price):
        try:
            if avg3m is not None and avg10d is not None and vol is not None:
                # Check if the day's volume is less than or equal to the average 10-day volume by a factor of 1.5x or more
                if float(vol) < float(avg10d) * 0.5:
                    hook = AsyncDiscordWebhook(below_avg_vol, content=f"<@1179080010724818954>")
                    embed = DiscordEmbed(title=f"Below Average Volume - {ticker}", description=f"```py\n{ticker} is currently trading BELOW AVERAGE VOLUME! by more than a factor of 1.5x", color=hex_colors['green'])
                    # Add fields to the embed
                    embed.add_embed_field(name=f"Day Stats:", value=f"> Open: **${r.web_stock_open}**\n> High: **${r.web_stock_high}**\n> Now: **${r.web_stock_close}**\n> Low: **${r.web_stock_low}**")
                    embed.add_embed_field(name=f"Volume Info:", value=f"> Today: **{round(float(vol)):,}**\n> Avg10D: **{round(float(avg10d)):,}**\n> Avg3M: **{round(float(avg3m)):,}**")
                    embed.add_embed_field(name=f"Volume Analysis:", value=f"> Buy: **{round(float(buyPct),2)}%**\n> Neut: **{round(float(neutPct),2)}%**\n> Sell: **{round(float(sellPct),2)}%**\n> Avg Price: **${avgPrice}**")
                    embed.set_footer(text=f"{ticker} | above avg. volume | {vol} | {avg10d}")
                    hook.add_embed(embed)
                    await self.insert_new_prices(ticker=ticker, type='below avg vol', fifty_high=r.fifty_high, price=r.web_stock_close, fifty_low=r.fifty_low, timestamp=timestamp)
                    await hook.execute()

                # Check if the day's volume is greater than or equal to the average 10-day volume by a factor of 1.5x or more
                elif float(vol) >= float(avg10d) * 1.5:
                    hook = AsyncDiscordWebhook(above_avg_vol, content=f"<@1179080010724818954>")
                    embed = DiscordEmbed(title=f"Above Average Volume - {ticker}", description=f"```py\n{ticker} is currently trading ABOVE AVERAGE VOLUME! by more than a factor of 1.5x", color=hex_colors['red'])
                    # Add fields to the embed
                    embed.add_embed_field(name=f"Day Stats:", value=f"> Open: **${r.web_stock_open}**\n> High: **${r.web_stock_high}**\n> Now: **${r.web_stock_close}**\n> Low: **${r.web_stock_low}**")
                    embed.add_embed_field(name=f"Volume Info:", value=f"> Today: **{round(float(vol)):,}**\n> Avg10D: **{round(float(avg10d)):,}**\n> Avg3M: **{round(float(avg3m)):,}**")
                    embed.add_embed_field(name=f"Volume Analysis:", value=f"> Buy: **{round(float(buyPct),2)}%**\n> Neut: **{round(float(neutPct),2)}%**\n> Sell: **{round(float(sellPct),2)}%**\n> Avg Price: **${avgPrice}**")
                    embed.add_embed_field(name=f"52week Stats:", value=f"> High: **${fifty_high}**\n> Now: **${r.web_stock_close}**\n> Low: **${fifty_low}**")
                    embed.set_footer(text=f"{ticker} | {price} | above avg. volume | {vol} | {avg10d}")
                    hook.add_embed(embed)
                    asyncio.create_task(self.insert_new_prices(ticker=ticker, type='above avg vol', fifty_high=r.fifty_high, price=r.web_stock_close, fifty_low=r.fifty_low, timestamp=timestamp))
                    await hook.execute()

        except Exception as e:
            # Handle or log the exception as needed
            print(f"An error occurred: {e}")
            return None

        return "Volume analysis completed"




    # Function to handle incoming WebSocket messages
            
    async def handle_msg(self, msgs: WebSocketMessage):
  
        monitor = EquityOptionTradeMonitor()
        
        for m in msgs:

         
            event_type = m.event_type
            if event_type == 'A' and m.symbol.startswith('I:'):
                async for data in self.db.insert_indices_aggs_second(m):
                    ticker = data.get('ticker')
                    print(f"INDICES PER SECOND: {ticker}")
                    last_five_trades = await monitor.repeated_hits(data)


                    if last_five_trades:
                        print(last_five_trades)


        
            if event_type == 'AM' and m.symbol.startswith('I:'):
                async for data in self.db.insert_indices_aggs_minute(m):
                    ticker = data.get('ticker')
                    print(f"INDICES - MINUTE {ticker}")




            #option aggs
            if event_type == 'A' and m.symbol.startswith('O:'):
                async for data in self.db.insert_option_aggs(m):
                    ticker = data.get('option_symbol')
                    print(f"OPTION AGGS {ticker}")



        

            #stock aggs
            if event_type == 'A' and not m.symbol.startswith('I:') and not m.symbol.startswith("O:"):
                async for data in self.db.insert_stock_aggs(m):
                    ticker = data.get('ticker')
                    
                    await self.queue.put(data)

                    asyncio.create_task(self.stock_rsi(ticker))
                    asyncio.create_task(self.stock_macd(ticker))


                    async for analysis_data, ticker_data, cost_data in self.stock_analysis(ticker):
                        print(analysis_data)

            #option trades
            if event_type == 'T' and m.symbol.startswith('O:'):
                async for data in self.db.insert_option_trades(m):
                    ticker = data.get('ticker')
                    print(f"OPTION TRADES: {ticker}")
                    # Call the repeated_hits method
                    last_five_trades = await monitor.repeated_hits(data)

                    # Check if the ticker has appeared 5 times in a row
                    if last_five_trades == 5:
                        embed = DiscordEmbed(title='Repeated Option Hits', description=f"# > {data.get('ticker')}")
                        print(f"{ticker} has appeared 5 times in a row.")
                        hook = AsyncDiscordWebhook(os.environ.get('repeated_hits'))
                        hook.add_embed(embed)
                        await hook.execute()









            #stock trades
            if event_type == 'T' and not m.symbol.startswith('O:') and not m.symbol.startswith('I:'):
                async for data in self.db.insert_stock_trades(m):
                    ticker = data.get('ticker')
                    print(f"STOCK TRADES: {ticker}")
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





            if event_type == 'XT':
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
                    

            if event_type == 'CAS':
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
            client = WebSocketClient(subscriptions=[pattern], api_key=os.environ.get('YOUR_POLYGON_KEY'), market=live_market)
            clients.append(client.connect(market.handle_msg))

    await asyncio.gather(*clients)  # Wait for all clients to finish



asyncio.run(main())

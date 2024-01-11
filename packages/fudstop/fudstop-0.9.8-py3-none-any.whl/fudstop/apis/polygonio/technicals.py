from fudstop.apis.polygonio.polygon_options import PolygonOptions
from fudstop.apis.polygonio.models.option_models.universal_snapshot import OptionData
from fudstop.apis.polygonio.async_polygon_sdk import Polygon
import asyncio
from fudstop.apis.discord_.discord_sdk import DiscordSDK
from fudstop._markets.list_sets.dicts import hex_color_dict
from fudstop.apis.polygonio.models.technicals import MACD,RSI,SMA,EMA
from fudstop._markets.list_sets.ticker_lists import most_active_tickers
import requests
discord = DiscordSDK()
from discord_webhook import AsyncDiscordWebhook, DiscordEmbed
opts = PolygonOptions(user='chuck', database='markets')
import os
import aiohttp
from dotenv import load_dotenv
load_dotenv()
poly = Polygon(connection_string=os.environ.get('POLYGON_STRING'))


from tabulate import tabulate
import asyncio
import pandas as pd




class Technicals:
    def __init__(self):
        self.opts = opts
        self.key = os.environ.get('DISCORD_AUTHORIZATION')
        self.discord = discord
        self.poly = poly

        self.macd_webhooks =  {
            'minute': os.environ.get('macd_minute'),
            'hour': os.environ.get('macd_hour'),
            'day': os.environ.get('macd_day'),
            'week': os.environ.get('macd_week'),
            'month': os.environ.get('macd_month'),
        }

    async def make_macd_channels(self, guild_id, channel_name, channel_description, with_webhook:bool=False, webhook_name:str='Spidey Bot'):
        """
        Makes MACD channels for your discord.
        """
        await self.discord.create_channel(guild_id=guild_id, channel_description=channel_description, channel_name=channel_name, with_webhook=with_webhook, webhook_name=webhook_name)

    async def get_macd(self, ticker, timespan):
        """
        Retrieves MACD data for a given ticker and timespan using Polygon.io.
        """
        macd_data = await self.poly.macd(ticker, timespan)
        return macd_data

    # Functions for EMA, SMA, RSI
    async def get_ema(self, ticker, timespan, short_window, long_window):
        """
        Retrieves EMA data for a given ticker and timespan using Polygon.io.
        """

        short_ema_data = await self.poly.ema(ticker, timespan, window=short_window)
        long_ema_data = await self.poly.ema(ticker, timespan, window=short_window)
        return short_ema_data, long_ema_data

    async def get_sma(self, ticker, timespan, short_window, long_window):
        """
        Retrieves SMA data for a given ticker and timespan using Polygon.io.
        """
        short_sma_data = await self.poly.sma(ticker, timespan, window=short_window)
        long_sma_data = await self.poly.sma(ticker, timespan, window=long_window)
        return short_sma_data,long_sma_data

    async def get_rsi(self, ticker, timespan):
        """
        Retrieves RSI data for a given ticker and timespan using Polygon.io.
        """
        rsi_data = await self.poly.rsi(ticker, timespan)
        return rsi_data
    


    async def detect_macd_cross(self, ticker, timespan):
        """
        Detect imminent MACD crossovers for a given ticker and timespan.
        """
        macd_data = await self.get_macd(ticker, timespan)
        if not hasattr(macd_data, 'macd_value'):
            return None

        # Check the last two data points for a crossover
        if len(macd_data.macd_value) >= 2:
            latest_macd = macd_data.macd_value[0]
            previous_macd = macd_data.macd_value[1]
            latest_signal = macd_data.macd_signal[0]
            previous_signal = macd_data.macd_signal[1]

            if previous_macd < previous_signal and latest_macd > latest_signal:
                return f"Bullish MACD Crossover for {ticker} on the {timespan}"
            elif previous_macd > previous_signal and latest_macd < latest_signal:
                return f"Bearish MACD Crossover for {ticker} on the {timespan}"

        return "No imminent MACD crossover detected"
    
    async def detect_ema_cross(self, ticker, short_window, long_window, timespan):
        """
        Detect imminent EMA crossovers for a given ticker, timespan, and window sizes.
        """
        short_ema_data, long_ema_data = await self.get_ema(ticker, timespan, short_window=short_window, long_window=long_window)


        # Check the last two data points for a crossover
        if len(short_ema_data.ema_value) >= 2 and len(long_ema_data.ema_value) >= 2:
            latest_short_ema = short_ema_data.ema_value[0]
            previous_short_ema = short_ema_data.ema_value[1]
            latest_long_ema = long_ema_data.ema_value[0]
            previous_long_ema = long_ema_data.ema_value[1]

            if previous_short_ema < previous_long_ema and latest_short_ema > latest_long_ema:
                return f"Bullish EMA Crossover for {ticker} on the {timespan} with lengths at: {short_window} / {long_window}"
            elif previous_short_ema > previous_long_ema and latest_short_ema < latest_long_ema:
                return f"Bearish EMA Crossover for {ticker} on the {timespan} with lengths at: {short_window} / {long_window}"

        return f"No imminent EMA crossover detected for {ticker} on the {timespan} with lengths at: {short_window} / {long_window}"

    async def detect_sma_cross(self, ticker, short_window, long_window, timespan):
        """
        Detect imminent SMA crossovers for a given ticker, timespan, and window sizes.
        """
        short_sma_data, long_sma_data = await self.get_sma(ticker, timespan, short_window=short_window,long_window=long_window)

        # Check the last two data points for a crossover
        if len(short_sma_data.sma_value) >= 2 and len(long_sma_data.sma_value) >= 2:
            latest_short_sma = short_sma_data.sma_value[0]
            previous_short_sma = short_sma_data.sma_value[1]
            latest_long_sma = long_sma_data.sma_value[0]
            previous_long_sma = long_sma_data.sma_value[1]

            if previous_short_sma < previous_long_sma and latest_short_sma > latest_long_sma:
                return f"Bullish SMA Crossover for {ticker} on the {timespan} with lengths at: {short_window} / {long_window}"
            elif previous_short_sma > previous_long_sma and latest_short_sma < latest_long_sma:
                return f"Bearish SMA Crossover for {ticker} on the {timespan} with lengths at: {short_window} / {long_window}"

        return f"No imminent SMA crossover detected for {ticker} on the {timespan} with lengths at: {short_window} / {long_window}"

technicals = Technicals()
sema = asyncio.Semaphore(2)
async def main(ticker, timespan, short_window:int=150, long_window:int=200):
    async with sema:
    
    
        short_ema_data, long_ema_data = await technicals.get_ema(ticker, timespan, short_window=short_window, long_window=long_window)
        short_sma_data, long_sma_data = await technicals.get_sma(ticker, timespan, short_window=short_window,long_window=long_window)
        rsi_data = await technicals.get_rsi(ticker, timespan)
        macd_data = await technicals.get_macd(ticker, timespan)

        if hasattr(rsi_data, 'rsi_data.rsi_value'):
            latest_rsi  = round(float(rsi_data.rsi_value[0]),5)
            rsi_timestamp = rsi_data.rsi_timestamp[0]

            print(f"RSI Value: {latest_rsi}")
            print(f"RSI Time: {rsi_timestamp}")



            if latest_rsi <= 30:
                print(f"RSI is oversold on the {timespan}")




        if hasattr(macd_data, 'macd_value'):
            macd_crossover = await technicals.detect_macd_cross(ticker, timespan)
            if 'No' not in macd_crossover and timespan in ['week', 'day', 'month']:
                hook = AsyncDiscordWebhook(os.environ.get('main_chat'), content=f"<@375862240601047070>")
                #hook = AsyncDiscordWebhook(technicals.macd_webhooks.get(timespan))
                


                df = pd.DataFrame(macd_data.as_dataframe)
                df['time'] = pd.to_datetime(df['time'])

                df['time'] = df['time'].dt.date
                df = df.head(10)
                # Rounding the values to a specified number of decimal places (e.g., 5)
                df['value'] = df['value'].round(3)
                df['signal'] = df['signal'].round(3)
                df['hist'] = df['hist'].round(3)
                # Adding a new column for the red cross marker
                # Convert the 'date' column to datetime format and reformat to YY/MM/DD
                df['time'] = pd.to_datetime(df['time']).dt.strftime('%y/%m/%d')

                # Identifying the rows where 'hist' changes from negative to positive
                hist_change = (df['hist'] > 0) & (df['hist'].shift(1) < 0)

                # Appending the red cross marker to the date
                df.loc[hist_change, 'time'] = df.loc[hist_change, 'time'] + ' ❌'

                df = df.drop(columns=['signal', 'time'])
                table = tabulate(df, headers='keys', tablefmt='fancy', showindex=False)



                emoji = "🐂" if 'Bullish' in macd_crossover else "🐻"
                color = hex_color_dict['red'] if emoji == "🐻" else hex_color_dict['green']
                embed = DiscordEmbed(title=f"MACD❌Crossover - {timespan}", description= f"# > {ticker} MACD CROSS - {timespan}\n_ _ _\n> MACD: **{round(float(macd_data.macd_value[0]),4)}**\n> SIGNAL: **{round(float(macd_data.macd_signal[0]),4)}**\n> HISTOGRAM: **{round(float(macd_data.macd_histogram[0]),4)}**\n_ _ _\n# > LAST 10 MEASURES:\n```py\n{table}```", color=color)
                embed.add_embed_field(name=f"<:_:1190025407815221270>", value=f"# > {ticker}")
                embed.set_footer(icon_url=os.environ.get('fudstop_logo'), text=f"Data by Polygon.io | Implemented by FUDSTOP")
                hook.add_embed(embed)
                await hook.execute()


        if long_ema_data is not None and long_sma_data is not None and short_ema_data is not None and short_sma_data is not None:

            ema_crossover = await technicals.detect_ema_cross(ticker, short_window=short_window, long_window=long_window, timespan=timespan)
            if 'No' not in ema_crossover:
                emoji = "🐂" if 'Bullish' in ema_crossover else "🐻"
                hook = AsyncDiscordWebhook(os.environ.get('main_chat'), content=f"<@1194516024859578428>")

                
                #await hook.execute()
                


            sma_crossover = await technicals.detect_sma_cross(ticker, short_window=short_window, long_window=long_window, timespan=timespan)
            if 'No' not in sma_crossover:
                emoji = "🐂" if 'Bullish' in ema_crossover else "🐻"
                hook = AsyncDiscordWebhook(os.environ.get('main_chat'), content=f"<@1194516024859578428>")
               # await hook.execute()
                


async def scan_technicals():
    timespans = ['minute', 'hour', 'day', 'week']
    tasks =[main(i, timespan) for i in most_active_tickers for timespan in timespans]

    await asyncio.gather(*tasks)


asyncio.run(scan_technicals())
                


# async def main2():
#     names = ["macd❌hour", "macd❌day", "macd❌week", "macd❌month"]
#     for name in names:
#         time = name.split('❌')[1]
        
#         discord.create_channel(guild_id=technicals.discord.fudstop_id, type='0',name=name, channel_description=f"Tickers that post here have just MACD crossed on the {time} timeframe. Green embeds = bullish. Red embeds = bearish. ❌", with_webhook=True, webhook_name=F'MACD CROSS - {time}')

#         await asyncio.sleep(10)


# asyncio.run(main2())
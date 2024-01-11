from apis.polygonio.polygon_database import PolygonDatabase
from polygon.websocket import WebSocketMessage
from apis.helpers import convert_to_ns_datetime
import os
import json
from datetime import datetime
from pytz import timezone
from apis.polygonio.mapping import stock_condition_desc_dict,stock_condition_dict,STOCK_EXCHANGES,OPTIONS_EXCHANGES, TAPES,option_condition_desc_dict,option_condition_dict,indicators,quote_conditions
import pandas as pd
from apis.helpers import get_human_readable_string, calculate_price_to_strike
utc = timezone('UTC')
import pytz
from pytz import timezone
aware_datetime = utc.localize(datetime.utcnow())
from .list_sets import crypto_conditions_dict, crypto_exchanges
class MarketDBManager(PolygonDatabase):
    def __init__(self, host, port, user, password, database, **kwargs):
        self.host=host
        self.port=port
        self.user=user
        self.password=password
        self.database=database
        super().__init__(host=host,port=port,database=database,password=password,user=user,**kwargs)


  

    async def insert_stock_trades(self, m):
        data = { 
            'type': 'EquityTrade',
            'ticker': m.symbol,
            'trade_exchange': STOCK_EXCHANGES.get(m.exchange),
            'trade_price': m.price,
            'trade_size': m.size,
            'trade_conditions': [stock_condition_dict.get(condition) for condition in m.conditions] if m.conditions is not None else [],
            'trade_timestamp': m.timestamp
        }


        df = pd.DataFrame(data)



        await self.batch_insert_dataframe(df, table_name='stock_trades', unique_columns='insertion_timestamp')
        yield data

    async def insert_crypto_trades(self, m):
        



        conditions = [crypto_conditions_dict.get(i) for i in m.conditions]
        data = { 
            'type': m.event_type,
            'ticker': m.pair,
            'exchange': crypto_exchanges.get(m.exchange),
            'id': m.id,
            'price': m.price,
            'size': m.size,
            'conditions': conditions,
        }

    
        df = pd.DataFrame(data, index=[0])
        await self.batch_insert_dataframe(df, table_name='crypto_trades', unique_columns='insertion_timestamp')
        yield data
    async def insert_forex_aggs(self, m):
        data_quotes= { 
            'open': m.open,
            'close': m.close,
            'ticker': m.pair,
            'high': m.high,
            'low': m.low,
            'volume': m.volume

        }
        df = pd.DataFrame(data_quotes, index=[0])
        await self.batch_insert_dataframe(df, table_name='forex_aggs', unique_columns='insertion_timestamp')

        yield data_quotes


    async def insert_stock_aggs(self, m):
        
        data = {
            'type': 'A',
            'ticker': m.symbol,
            'close_price': m.close,
            'high_price': m.high,
            'low_price': m.low,
            'open_price': m.open,
            'volume': m.volume,
            'official_open': m.official_open_price,
            'accumulated_volume': m.accumulated_volume,
            'vwap_price': m.vwap,
            'agg_timestamp': m.end_timestamp
        }
        
        df = pd.DataFrame(data, index=[0])
        await self.batch_insert_dataframe(df, table_name='stock_aggs', unique_columns='insertion_timestamp')
        yield data

    async def insert_stock_quotes(self, m):
        
        indicator = [indicators.get(indicator) for indicator in m.indicators] if m.indicators is not None else []
        data = {
        'type': 'Q',
        'ticker': m.symbol,
        'ask': m.ask_price,
        'bid':m.bid_price,
        'ask_size': m.ask_size,
        'bid_size':m.bid_size,
        'indicator': indicator,
        'condition':quote_conditions.get(m.condition),

        
        'ask_exchange':STOCK_EXCHANGES.get(m.ask_exchange_id),
        'bid_exchange':STOCK_EXCHANGES.get(m.bid_exchange_id),
        
        'timestamp': m.timestamp,
        'tape': TAPES.get(m.tape)}

        df = pd.DataFrame(data)

        await self.batch_insert_dataframe(df, table_name='stock_quotes', unique_columns='insertion_timestamp')
        yield data
    async def insert_option_aggs(self, m):
 
        us_central = pytz.timezone('US/Central')
        utc = pytz.UTC
        symbol = get_human_readable_string(m.symbol)
        strike = symbol.get('strike_price')
        expiry = symbol.get('expiry_date')
        call_put = symbol.get('call_put')
        underlying_symbol = symbol.get('underlying_symbol')
        trade_message_data = {}
        trade_message_data['type'] = 'EquityOptionTrade'
        trade_message_data['expiry'] = expiry
        trade_message_data['expiry'] =  datetime.strptime(expiry, '%Y-%m-%d').date()
        trade_message_data['call_put'] = call_put
        trade_message_data['underlying_symbol'] = underlying_symbol
        trade_message_data['strike'] = strike
        

        trade_message_data['option_symbol'] = m.symbol
        trade_message_data['price'] = m.price
        trade_message_data['size'] = m.size
        

        
        trade_message_data['price_to_strike'] = calculate_price_to_strike(m.price, strike)


        timestamp = datetime.fromtimestamp(m.timestamp / 1000.0, tz=utc)
        naive_utc_datetime = aware_datetime.astimezone(timezone('UTC')).replace(tzinfo=None)
        trade_message_data['hour_of_day'] = timestamp.hour

        # Now, keep the timestamp in Eastern Time
        trade_message_data['timestamp'] = naive_utc_datetime

        trade_message_data['conditions'] = [option_condition_dict.get(condition) for condition in m.conditions] if m.conditions is not None else []
        trade_message_data['conditions'] = trade_message_data['conditions'][0]
        trade_message_data['weekday'] = timestamp.weekday()
        trade_message_data['exchange'] = OPTIONS_EXCHANGES.get(m.exchange)


 

        df = pd.DataFrame(trade_message_data)
        await self.batch_insert_dataframe(df, table_name='option_trades', unique_columns='insertion_timestamp')
        return trade_message_data


    async def insert_option_trades(self, m):

        df = pd.DataFrame(vars(m), index=[0])
        await self.batch_insert_dataframe(df, table_name='option_aggs', unique_columns='insertion_timestamp')
        yield df.to_dict()



    async def insert_indices_aggs_minute(self, m):
        

        data_queue_data = { 
            'type': 'AM',
            'ticker': m.symbol,
            'day_open': m.official_open_price,
            'minute_open': m.open,
            'minute_high': m.high,
            'minute_low': m.low,
            'minute_close': m.close,
            'minute_start': m.start_timestamp,
            'minute_end': m.end_timestamp
        }


        df = pd.DataFrame(data_queue_data, index=[0])

        await self.batch_insert_dataframe(df, table_name='indices_aggs_minute', unique_columns='insertion_timestamp')      

        
        yield data_queue_data


    async def insert_indices_aggs_second(self, m):
        

        data_queue_data = { 
            'type': 'A',
            'official_open': m.official_open_price,
            'ticker': m.symbol,
            'open': m.open,
            'high': m.high,
            'low': m.low,
            'close': m.close,
            'minute_start': m.start_timestamp,
            'minute_end': m.end_timestamp
        }


        df = pd.DataFrame(data_queue_data, index=[0])

        await self.batch_insert_dataframe(df, table_name='indices_aggs_second', unique_columns='insertion_timestamp')      

        
        yield data_queue_data






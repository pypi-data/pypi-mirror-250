from apis.polygonio.polygon_database import PolygonDatabase
from polygon.websocket import WebSocketMessage
from apis.helpers import convert_to_ns_datetime
import os
import json
from datetime import datetime
from pytz import timezone
from apis.polygonio.mapping import stock_condition_desc_dict,stock_condition_dict,STOCK_EXCHANGES,OPTIONS_EXCHANGES,option_condition_desc_dict,option_condition_dict,indicators,quote_conditions
import pandas as pd
utc = timezone('UTC')
aware_datetime = utc.localize(datetime.utcnow())
from .list_sets import crypto_conditions_dict, crypto_exchanges
class MarketDBManager(PolygonDatabase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


  

    async def insert_stock_trades(self, m):
        m.condition = stock_condition_dict.get(m.conditions)
        df = pd.DataFrame(vars(m), index=[0])





        await self.batch_insert_dataframe(df, table_name='stock_trades', unique_columns='insertion_timestamp')
        yield m

    async def insert_crypto_trades(self, m):
        



        conditions = [crypto_conditions_dict.get(i) for i in m.conditions]
        data = { 
            'type': m.event_type,
            'symbol': m.pair,
            'exchange': crypto_exchanges.get(m.exchange),
            'id': m.id,
            'price': m.price,
            'size': m.size,
            'conditions': conditions[0],
        }

    
        df = pd.DataFrame(data, index=[0])
        await self.batch_insert_dataframe(df, table_name='crypto_trades', unique_columns='insertion_timestamp')
        yield data
    async def insert_forex_aggs(self, m):
        data_quotes= { 
            'open': m.open,
            'close': m.close,
            'pair': m.pair,
            'high': m.high,
            'low': m.low,
            'volume': m.volume

        }
        df = pd.DataFrame(data_quotes, index=[0])
        await self.batch_insert_dataframe(df, table_name='forex_aggs', unique_columns='insertion_timestamp')

        yield data_quotes


    async def insert_stock_aggs(self, m):
        
        df = pd.DataFrame(vars(m), index=[0])
        await self.batch_insert_dataframe(df, table_name='stock_aggs', unique_columns='insertion_timestamp')
        yield m

    async def insert_stock_quotes(self, m):
        
        m.indicators = ','.join(map(str, m.indicators)) if m.indicators is not None else None
        m.indicators = indicators.get(m.indicators)
        df = pd.DataFrame(vars(m), index=[0])
        await self.batch_insert_dataframe(df, table_name='stock_quotes', unique_columns='insertion_timestamp')
        yield m
    async def insert_option_aggs(self, m):

        
        df = pd.DataFrame(vars(m), index=[0])
        await self.batch_insert_dataframe(df, table_name='option_aggs', unique_columns='insertion_timestamp')
        yield m

    async def insert_option_trades(self, m):
        

        m.conditions = ','.join(map(str, m.conditions))
        m.condition = option_condition_dict.get(m.conditions)
        df = pd.DataFrame(vars(m), index=[0])
        await self.batch_insert_dataframe(df, table_name='option_trades', unique_columns='insertion_timestamp')

        yield m
    async def insert_indices_aggs(self, m):
        

        data_queue_data = { 
            'type': 'Indices',
            'ticker': m.symbol,
            'day_open': m.official_open_price,
            'minute_open': m.open,
            'minute_high': m.high,
            'minute_low': m.low,
            'minute_close': m.close,
            'minute_start': convert_to_ns_datetime(m.start_timestamp),
            'minute_end': convert_to_ns_datetime(m.end_timestamp)
        }


        df = pd.DataFrame(data_queue_data, index=[0])

        await self.batch_insert_dataframe(df, table_name='indices_aggs', unique_columns='insertion_timestamp')      

        
        yield data_queue_data





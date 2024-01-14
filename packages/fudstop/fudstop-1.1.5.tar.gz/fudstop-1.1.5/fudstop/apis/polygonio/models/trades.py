from mapping import stock_condition_dict, STOCK_EXCHANGES, TAPES
from datetime import datetime
import pytz
from dataclasses import dataclass
import pandas as pd
class TradeData:
    def __init__(self, data, ticker):
        self.conditions = [i.get('conditions') for i in data]
        self.conditions = [item for sublist in (self.conditions or []) if sublist is not None for item in sublist]
        self.conditions = [stock_condition_dict.get(cond) for cond in self.conditions]
        
        self.exchange = [STOCK_EXCHANGES.get(i.get('exchange')) for i in data]
        self.id = [i.get('id') for i in data]
        self.price = [i.get('price') for i in data]
        self.sequence_number = [i.get('sequence_number') for i in data]
        self.sip_timestamp = [i.get('sip_timestamp') for i in data]
        self.size = [i.get('size') for i in data]
        self.tape = [TAPES.get(i.get('tape')) for i in data]

        self.align_list_lengths()
        self.data_dict = { 
            'sequence_number': self.sequence_number,
            'conditions': self.conditions,
            'exchange': self.exchange,
            'id': self.id,
            'trade_size': self.size,
            'trade_price': self.price,
            'tape': self.tape

        }

        self.df = pd.DataFrame(self.data_dict)
        self.ticker = ticker

    @staticmethod
    async def convert_timestamp(ts):
        # Convert nanoseconds to seconds
        timestamp_in_seconds = ts / 1e9
        # Convert to datetime object in UTC
        dt_utc = datetime.utcfromtimestamp(timestamp_in_seconds)
        # Convert to Eastern Time
        eastern = pytz.timezone('US/Eastern')
        dt_eastern = dt_utc.replace(tzinfo=pytz.utc).astimezone(eastern)
        # Format as a string
        return dt_eastern.strftime('%Y-%m-%d %H:%M:%S')
    @staticmethod
    def flatten(lst):
        return [item for sublist in lst for item in (sublist if isinstance(sublist, list) else [sublist])]
    


    def align_list_lengths(self):
        # Find the maximum length among all attributes
        max_length = max(len(getattr(self, attr)) for attr in ['sequence_number', 'conditions', 'exchange', 'id', 'size', 'price', 'tape'])

        # Extend shorter lists to match the maximum length
        for attr in ['sequence_number', 'conditions', 'exchange', 'id', 'size', 'price', 'tape']:
            current_list = getattr(self, attr)
            current_list.extend([None] * (max_length - len(current_list)))
            setattr(self, attr, current_list)
    @staticmethod
    def ensure_list(value):
        if isinstance(value, list):
            return value
        else:
            return [value]
    def __repr__(self):
        return f"<TradeData id={self.id}, price={self.price}, size={self.size}>"
    
from typing import Optional,Any,Dict

@dataclass
class LastTradeData:
    def __init__(self, results):

        if results is not None:
            self.ticker = results.get('T', None)

            self.exchange = STOCK_EXCHANGES.get(results.get('x'))
            self.conditions = [stock_condition_dict.get(i) for i in results.get('c')]

            self.price = results.get('p')
            self.size = results.get('s')
            self.correction = results.get('e')
            self.sequence_number = results.get('q')
            self.tape = TAPES.get(results.get('z'))
            self.dollar_cost = self.price * self.size if self.price is not None and self.size is not None and self.price != 0 and self.size != 0 else 0

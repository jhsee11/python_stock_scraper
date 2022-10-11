import yahoo_fin.stock_info as si
import pandas as pd
from stock_info_collector import StockInfoCollector

class QuoteTableCollector(StockInfoCollector):
    def __init__(self, stock_list):
        super().__init__(stock_list)
        self.collection = self.db["Company_QuoteTable"]

    def collect_quote_table(self):
        for ticker in self.stock_list:
            quote_table = si.get_quote_table(ticker)
            quote_table['ticker'] = ticker
            # insert data into table
            self.collection.insert_one(quote_table)

    def retrieve_quote_table(self, ticker):
        # extract data from mongo db
        data_from_db = self.collection.find({"ticker": ticker})
        df = pd.DataFrame(data_from_db)
        return df

s = QuoteTableCollector(['AAPL'])
s.collect_quote_table()
import yahoo_fin.stock_info as si
import pandas as pd
from stock_info_collector import StockInfoCollector

class StatsValCollector(StockInfoCollector):
    def __init__(self, stock_list):
        super().__init__(stock_list)
        self.collection = self.db["Company_StatsVal"]

    def collect_stats_valuation(self):
        #dow_stats = {}
        for ticker in self.stock_list:
            temp = si.get_stats_valuation(ticker)
            temp = temp.iloc[:, :2]
            temp.columns = ["Attribute", "Recent"]
            #temp.reset_index(inplace=True)
            # transposed["ticker"] = ticker
            temp.insert(loc=0, column='ticker', value=[ticker for _ in range(temp.shape[0])])
            data_dict = temp.to_dict("records")
            self.collection .insert_many(data_dict)

    def retrieve_stats_val(self, ticker):
        # extract data from mongo db
        data_from_db = self.collection.find({"ticker": ticker})
        df = pd.DataFrame(data_from_db)
        return df

s = StatsValCollector(['AAPL'])
s.collect_stats_valuation()
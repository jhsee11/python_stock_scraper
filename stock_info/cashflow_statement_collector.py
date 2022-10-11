import yahoo_fin.stock_info as si
import pandas as pd
from stock_info_collector import StockInfoCollector

class CashflowStatementCollector(StockInfoCollector):
    def __init__(self, stock_list):
        super.__init__(stock_list)
        self.collection = self.db["Company_CashFlowStatement"]

    def collect_cashflow_statement(self):
        for ticker in self.stock_list:
            # get the cashflow statement
            cashflow_statement = si.get_cash_flow(ticker)
            cashflow_statement = cashflow_statement.transpose()
            cashflow_statement.reset_index(inplace=True)
            cashflow_statement.insert(loc=0, column='ticker',
                                      value=[ticker for _ in range(cashflow_statement.shape[0])])
            data_dict = cashflow_statement.to_dict("records")
            # insert into mongodb
            self.collection.insert_many(data_dict)

    def retrieve_cashflow_statement(self, ticker):
        # extract data from mongo db
        data_from_db = self.collection.find({"ticker": ticker})
        df = pd.DataFrame(data_from_db)
        return df

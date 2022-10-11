from pymongo import MongoClient
import yahoo_fin.stock_info as si
import pandas as pd

class StockInfoCollector:
    def __init__(self, stock_list):
        # Making a Connection with MongoClient
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["stocks_database"]
        self.stock_list = stock_list

    def collect_balance_sheet(self):
        dow_stats = {}
        collection = self.db["Company_BalanceSheet"]
        for ticker in self.stock_list:
            # get the balance sheet
            balance_sheet = si.get_balance_sheet(ticker)
            balance_sheet = balance_sheet.transpose()
            balance_sheet.reset_index(inplace=True)
            # transposed["ticker"] = ticker
            balance_sheet.insert(loc=0, column='ticker', value=[ticker for _ in range(balance_sheet.shape[0])])
            data_dict = balance_sheet.to_dict("records")
            collection.insert_many(data_dict)

    def retrieve_balance_sheet(self, ticker):
        # extract data from mongo db
        collection = self.db["Company_BalanceSheet"]
        data_from_db = collection.find({"ticker": ticker})
        df = pd.DataFrame(data_from_db)
        return df

    def collect_income_statement(self):
        collection = self.db["Company_IncomeStatement"]
        for ticker in self.stock_list:
            # get the income statement
            income_statement = si.get_income_statement(ticker)
            transposed = income_statement.transpose()
            transposed.reset_index(inplace=True)
            # transposed["ticker"] = ticker
            transposed.insert(loc=0, column='ticker', value=[ticker for _ in range(transposed.shape[0])])
            data_dict = transposed.to_dict("records")
            collection.insert_many(data_dict)

    def retrieve_income_statement(self, ticker):
        # extract data from mongo db
        collection = self.db["Company_BalanceSheet"]
        data_from_db = collection.find({"ticker": ticker})
        df = pd.DataFrame(data_from_db)
        return df

    def collect_cashflow_statement(self):
        collection = self.db["Company_CashFlowStatement"]
        for ticker in self.stock_list:
            # get the cashflow statement
            cashflow_statement = si.get_cash_flow(ticker)
            cashflow_statement = cashflow_statement.transpose()
            cashflow_statement.reset_index(inplace=True)
            cashflow_statement.insert(loc=0, column='ticker',
                                      value=[ticker for _ in range(cashflow_statement.shape[0])])
            data_dict = cashflow_statement.to_dict("records")
            # insert into mongodb
            cashflow_statement.insert_many(data_dict)



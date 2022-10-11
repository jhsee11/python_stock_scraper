import stock_info_collector
from stock_ohlc_collector import StockOhlcCollector

s = StockOhlcCollector(['AMZN','AAPL','V'])
s.collect_ohlc()
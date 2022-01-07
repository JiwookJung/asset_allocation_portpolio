# Used FinanceDataReader
# https://github.com/FinanceData/FinanceDataReader

# TODO: restruct VAA module
# TODO: exceptions for holiday

# aggressive VAA strategy implementation
# https://www.youtube.com/c/%ED%95%A0%EC%88%98%EC%9E%88%EB%8B%A4%EC%95%8C%EA%B3%A0%ED%88%AC%EC%9E%90


import FinanceDataReader as fdr
import logging
from datetime import date, timedelta
import numpy as np

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_hander = logging.StreamHandler()
logger.addHandler(stream_hander)

class NASDAQStockList:
    MONTH_EARLY = [30,91,182,365]
    WEIGHT = [12.0,6.0,3.0,1.0]
    offensive_etf = ["SPY", "EFA", "EEM", "AGG"]
    defensive_etf = ["LQD","IEF","SHY"]
    def __init__(self, market = 'NASDAQ'):
        self.fdf = fdr.StockListing(market)
        self.yesterday = date.today() - timedelta(1)

    def get_stock_list(self):
        return self.fdf

    def get_stock_data(self, symbol, start_year=None, end_year=None):
        try:
            return fdr.DataReader(symbol=symbol, start=start_year, end=end_year)
        except Exception as e:
            logger.error(e)

    def get_momentum_score(self, e):
        stock.get_stock_data(e, start_year=2020, end_year=2021)
        stock_data = stock.get_stock_data(e)
        yesterday_close = stock_data['Close'][self.yesterday.strftime("%Y-%m-%d")]
        rate = []
        for i in self.MONTH_EARLY:
            target_date = self.yesterday - timedelta(i)
            close = stock_data['Close'][target_date.strftime("%Y-%m-%d")]
            rate.append( (yesterday_close - close)/close )
        score = np.dot(np.array(self.WEIGHT), np.array(rate))
        # print(score)
        return  score

    def get_offensive_momentum(self):
        res = []
        for e in self.offensive_etf:
            s = stock.get_momentum_score(e)
            res.append(s)
        print(res)
        return res

    def get_defensive_momentum(self):
        res = []
        for e in self.defensive_etf:
            s = stock.get_momentum_score(e)
            res.append(s)
        print(res)
        return res

if __name__ == '__main__':

    stock = NASDAQStockList()
    os = stock.get_offensive_momentum()

    os_check = [True if i >0 else False for i in os]
    if all(os_check):
        logger.info(f"BUY {stock.offensive_etf[os.index(max(os))]}")
    else:
        ds = stock.get_defensive_momentum()
        logger.info(f"BUY {stock.defensive_etf[ds.index(max(ds))]}")


import FinanceDataReader as fdr
import logging
from datetime import timedelta
import datetime
import numpy as np
from pandas.tseries.offsets import BDay

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_hander = logging.StreamHandler()
logger.addHandler(stream_hander)

class Strategy:
    def __init__(self):
        self.current_date = datetime.datetime.now()
        self.this_year = self.current_date.year
        self.last_year = self.this_year - 1
        self.last_day = (self.current_date - BDay(1)).date()

    def get_stock_data(self, symbol):
        try:
            return fdr.DataReader(symbol=symbol, start=str(self.last_year), end=self.current_date.strftime("%Y-%m-%d"))
        except Exception as e:
            logger.error(e)

    def get_momentum_weighted_score(self, e):
        logger.debug(e)
        stock_data = self.get_stock_data(e)
        last_close = stock_data['Close'][self.last_day.strftime("%Y-%m-%d")]
        rate = []
        for i in self.MONTH_EARLY:
            # get business day from timedelta
            target_date = self.current_date - timedelta(i) - BDay(0)
            close = stock_data['Close'][target_date.strftime("%Y-%m-%d")]
            rate.append( (last_close - close)/close )
        score = np.dot(np.array(self.WEIGHT), np.array(rate))
        return score

    def get_momentum(self, etf_list):
        res = {}
        for e in etf_list:
            s = self.get_momentum_weighted_score(e)
            res[e] = s
        logger.debug(res)
        return res

    def get_price_per_ma(self, e, days):
        logger.debug(e)
        stock_data = self.get_stock_data(e)
        ma = stock_data['Close'].rolling(window=days).mean() # moving average line
        last_ma5 = ma[self.last_day.strftime("%Y-%m-%d")]
        last_close = stock_data['Close'][self.last_day.strftime("%Y-%m-%d")]
        return last_close/last_ma5

    def get_ma_year(self, etf_list):
        res = {}
        for e in etf_list:
            s = self.get_price_per_ma(e, 260)
            res[e] = s
        return res
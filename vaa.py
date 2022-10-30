# Used FinanceDataReader
# https://github.com/FinanceData/FinanceDataReader

# aggressive VAA strategy implementation
# https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3002624
# https://www.youtube.com/c/%ED%95%A0%EC%88%98%EC%9E%88%EB%8B%A4%EC%95%8C%EA%B3%A0%ED%88%AC%EC%9E%90

import logging
from pandas.tseries.offsets import BDay
from strategy import Strategy

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_hander = logging.StreamHandler()
logger.addHandler(stream_hander)

class StrategyVAA(Strategy):
    MONTH_EARLY = [30,91,182,365]
    WEIGHT = [12.0,6.0,3.0,1.0]
    offensive_etf = ["SPY", "EFA", "EEM", "AGG"]
    defensive_etf = ["LQD","IEF","SHY"]

    def __init__(self):
        logger.info("================== Init VAA ====================")
        super().__init__()

    def calculate(self, total_asset):
        logger.info("-------------------- Calculate VAA Start --------------------")
        om = self.get_momentum(self.offensive_etf)

        om_check = [True if v > 0 else False for k, v in om.items()]
        if all(om_check):
            logger.info(f"* BUY  {om[max(om, key=om.get)]} {total_asset}")
        else:
            dm = self.get_momentum(self.defensive_etf)
            logger.info(f"* BUY  {dm[max(dm, key=dm.get)]} {total_asset}")

        logger.info("-------------------- Calculate VAA Done --------------------")

if __name__ == '__main__':
    stock = StrategyVAA()
    total_asset = 10000
    stock.calculate(total_asset)


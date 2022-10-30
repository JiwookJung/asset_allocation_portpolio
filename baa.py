# Used FinanceDataReader
# https://github.com/FinanceData/FinanceDataReader

# TODO: restruct BAA module
# TODO: exceptions for holiday

# aggressive BAA strategy implementation
# https://www.youtube.com/watch?v=CclFfZVSx9k

import logging
from pandas.tseries.offsets import BDay
from operator import itemgetter
from strategy import Strategy

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_hander = logging.StreamHandler()
logger.addHandler(stream_hander)

class StrategyBAA(Strategy):
    MONTH_EARLY = [30,91,182,365]
    WEIGHT = [12.0,6.0,3.0,1.0]
    offensive_etf = ["SPY", "QQQ", "IWM", "VGK", "EWJ", "VWO", "VEA", "VNQ", "DBC", "GLD", "LQD", "HYG"]
    alt_etf = ["VNQ", "DBC", "GLD"] 
    defensive_etf = ["BIL","IEF","TLT", "LQD", "TIP", "BND", "DBC"]
    # defensive_etf = ["BIL","IEF","TLT", "LQD", "HYG", "TIP", "BND"]
    canaria_etf = ["SPY", "VEA", "VWO", "BND"]

    def __init__(self):
        logger.info("==================== Init BAA ====================")
        super().__init__()

    def calculate(self, total_asset):
        logger.info("-------------------- Calculate BAA Start --------------------")
        cm = self.get_momentum(self.canaria_etf)
        logger.debug(cm)
        cm_check = [True if v > 0 else False for k, v in cm.items()]

        if all(cm_check):     # BUY offensive
            logger.info("BUY offensive")
            om = self.get_momentum(self.offensive_etf)
            cnt = sum(1 if v > 0 else 0 for k, v in om.items())
            if cnt >= 6:
                offensive_ratio = 1
            else:
                offensive_ratio = cnt/6
            
            defensive_ratio = 1 - offensive_ratio
            logger.info(f"offensive {cnt} etfs")

            res = dict(sorted(om.items(), key = itemgetter(1), reverse = True)[:cnt])
            [logger.info(f"* BUY {k} {1/6 * total_asset}") for k, v in res.items()]
            if cnt < 6:
                logger.info(f"offensive ratio:{offensive_ratio} defensive ratio:{defensive_ratio}")
                dm = self.get_ma_year(self.defensive_etf)
                res = dict(sorted(dm.items(), key = itemgetter(1), reverse = True)[:3])
                [logger.info(f"* BUY BIL {1/3*defensive_ratio * total_asset}") if v < 1 else logger.info(f"* BUY {k} {1/3*defensive_ratio * total_asset}") for k, v in res.items()]
        else:    # BUY only defensive
            logger.info("only defensive")
            dm = self.get_ma_year(self.defensive_etf)
            res = dict(sorted(dm.items(), key = itemgetter(1), reverse = True)[:3])
            [logger.info(f"* BUY BIL {1/3 * total_asset}") if v < 1 else logger.info(f"* BUY {k} {1/3 * total_asset}") for k, v in res.items()]

        logger.info("-------------------- Calculate BAA Done --------------------")


if __name__ == '__main__':
    stock = StrategyBAA()
    # dollar
    total_asset = 10000
    stock.cacluate(total_asset)

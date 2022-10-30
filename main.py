import FinanceDataReader as fdr
from vaa import StrategyVAA
from baa import StrategyBAA

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_hander = logging.StreamHandler()
logger.addHandler(stream_hander)

if __name__ == '__main__':
    strategies = ['VAA', 'BAA']
    total_asset = 10000
    market = 'NASDAQ'
    fdf = fdr.StockListing(market)
    
    for strategy in strategies:
        if strategy == 'VAA':
            stock = StrategyVAA()
            stock.calculate(total_asset)

        elif strategy == 'BAA':
            stock = StrategyBAA()
            stock.calculate(total_asset)
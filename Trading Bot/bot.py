import backtrader as bt
import datetime
from strategy2 import MA_CrossOver


cerebro = bt.Cerebro()

cerebro.broker.set_cash(10000)

data = bt.feeds.YahooFinanceCSVData(
    dataname = 'oracle.csv'

)
cerebro.adddata(data)
cerebro.addstrategy(MA_CrossOver)
cerebro.addsizer(bt.sizers.FixedSize, stake=500)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run()

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())


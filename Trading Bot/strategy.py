from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt
import backtrader.indicators as btind


class MA_CrossOver(bt.Strategy):

    alias = ('SMA_CrossOver',)

    params = (
        # period for the fast Moving Average
        ('fast', 6),
        # period for the slow moving average
        ('slow', 14),
        # moving average to use
        ('_movav', btind.MovAv.SMA)
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
    def __init__(self):
        sma_fast = self.p._movav(period=self.p.fast)
        sma_slow = self.p._movav(period=self.p.slow)
        self.dataclose = self.datas[0].close
        self.order = None

        self.buysig = btind.CrossOver(sma_fast, sma_slow)
        self.sellsig = btind.PercentChange() == 5

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     ))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          ))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None
    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])
        print(len(self))
        print(self.order)
        print(self.position)
        if self.order:
            return
        if not self.position:
            if self.buysig:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()

        else:
            if len(self) >= (self.bar_executed + 5) and self.sellsig:
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()
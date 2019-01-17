import os, sys, signal, time

from threading import Thread

from allTrades import AllTrades
from graph import Graph
from connector import Connector


class Trader(Graph, AllTrades, Connector):

    def __init__(self):
        self.disableLogging()

        try:
            TradeDataSource = Thread(target=self.getDataSource, args=(self.allTradesCallback,))
            TradeDataSource.daemon = True
            TradeDataSource.start()
            GraphData = Thread(target=self.getData, args=(self.graphCallback,))
            GraphData.daemon = True
            GraphData.start()
            LevelII = Thread(target=self.subscribeQuoteLevelII, args=(self.levelIICallback,))
            LevelII.daemon = True
            LevelII.start()
            while True: time.sleep(100)
        except (KeyboardInterrupt, SystemExit):
            print '\n! Received keyboard interrupt, quitting threads.\n'

    def clear(self):
        pass

    def disableLogging(self):
        sys.stdout = open(os.devnull, 'w')

    def enableLogging(self):
        sys.stdout = sys.__stdout__

    def allTradesCallback(self, trade):
        if trade.flags == 1:
            self.updateOfferSide(trade)
        else:
            self.updateBidSide(trade)
        # self.enableLogging()
        # print 'allTradesCallback', trade
        # self.disableLogging()

    def graphCallback(self):
        pass
        # self.enableLogging()
        # print 'graphCallback'
        # self.disableLogging()

    def levelIICallback(self):
        pass
        # self.enableLogging()
        # print 'levelIICallback'
        # self.disableLogging()

if __name__ == "__main__":
    robot = Trader()

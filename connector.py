# -*- coding: utf-8 -*-
#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#
import os
import sys
import time
import zmq

from threading import Thread
from decimal import Decimal
from request import Request
from allTrades import AllTrades

# client.plain_username = 'U0134277'
# client.plain_password = '02318'


class Connector(Request, AllTrades):
    sys.path.insert(0, './api')

    ctx = zmq.Context.instance()
    client = ctx.socket(zmq.REQ)
    client.connect('tcp://127.0.0.1:5560')

    bidsStack = {}
    offersStack = {}

    amountOffersAndBids = 0

    bidsStackLevelII = {}
    offersStackLevelII = {}

    def clear(self): return os.system('cls')

    def subscribeQuoteLevelII(self, cb=None):
        socket = self.ctx.socket(zmq.SUB)
        socket.connect('tcp://127.0.0.1:5561')
        socket.subscribe('24')

        should_continue = True
        while should_continue:
            messageNumber = socket.recv()
            messageResult = socket.recv()
            self.getQuoteLevelII()
            if cb:
                cb()

    def allTradesCallback(self, trade):
        if trade.flags == 1:
            self.updateBidSide(trade)
        else:
           self.updateOfferSide(trade)

        self.getQuoteLevelII()

    def subscribeQuoteLevelIIWithAllTrades(self):
        try:
            TradeDataSource = Thread(target=self.getDataSource,
                                     args=(self.allTradesCallback,))
            TradeDataSource.daemon = True
            TradeDataSource.start()
            # self.subscribeQuoteLevelII()
            while True:
                time.sleep(100)
        except (KeyboardInterrupt, SystemExit):
            print '\n! Received keyboard interrupt, quitting threads.\n'

    def getQuoteLevelII(self):
        request = self.fetchQuoteLevelIIConnector()
        self.client.send(request)
        message = self.client.recv()
        messageResult = self.parseQuoteLevelIIConnector(message)
        self.clear()
        self.calculateSpread(messageResult.offers, messageResult.bids)
        self.amountLevelII(messageResult.offers, messageResult.bids)
        self.updateOfferStack(messageResult.offers)
        self.updateBidStack(messageResult.bids)

    def calculateSpread(self, offers, bids):
        """ Считает спред """
        offerPrices = sorted(map(lambda offer: float(offer.price), offers))
        bidPrices = sorted(map(lambda bid: float(bid.price), bids))

        offerBestPrice = offerPrices[0]
        bidBestPrice = bidPrices[len(bidPrices) - 1]
        print 'spread ', offerBestPrice - bidBestPrice

    def amountLevelII(self, offers, bids):
        """ Суммирует объем по всем заявкам """

        offerQuantity = 0
        for offerIndex in range(len(offers)):
            offerQuantity += int(offers[offerIndex].quantity)

        bidQuantity = 0
        for bidIndex in range(len(bids)):
            bidQuantity += int(bids[bidIndex].quantity)

        self.amountOffersAndBids = offerQuantity + bidQuantity

    def updateOfferStack(self, offers):
        """ Содержит заявки на продажи с их измененным состоянием относительно пред. изменения """
        offersPrice = []
        for offerIndex in range(len(offers)):
            offersPrice.append(offers[offerIndex].price)

        offersStackCopy = {}
        for offerPriceIndex in range(len(offersPrice)):
            price = offersPrice[offerPriceIndex]
            if price in self.offersStack:
                offersStackCopy.update({price: self.offersStack[price]})

        offersStack = dict(offersStackCopy)
        for offerIndex in range(len(offers)):
            offer = offers[offerIndex]
            offerStack = self.offersStack.get(offer.price)
            change = 0

            if offerStack:
                change = 100 * (int(offer.quantity) -
                                offerStack.get('value')) / offerStack.get('value')
                ratio = 100 * int(offer.quantity) / self.amountOffersAndBids
                maxValue = int(offer.quantity) if int(offer.quantity) > offerStack.get(
                    'maxValue') else offerStack.get('maxValue')
                inserter = {}
                inserterChild = {
                    'value': int(offer.quantity),
                    'prevValue': int(offerStack.get('value')),
                    'maxValue': maxValue,
                    'change': change,
                    'ratio': ratio,
                    'tradesQty': int(offerStack.get('tradesQty'))
                }
                inserter[offer.price] = inserterChild
                offersStack.update(inserter)
            else:
                ratio = 100 * int(offer.quantity) / self.amountOffersAndBids
                offersStack.update(
                    {offer.price: {'value': int(offer.quantity), 'change': 0, 'ratio': ratio, 'maxValue': int(offer.quantity), 'tradesQty': 0}})
        self.offersStackLevelII = offersStack.copy()
        self.offersStack = offersStack.copy()
        print 'change offer ---'
        for key in sorted(offersStack, reverse=True):
            print "%s: %s" % (key, offersStack[key])

    def updateBidStack(self, bids):
        """ Содержит заявки на покупки с их измененным состоянием относительно пред. изменения """
        bidsPrice = []
        for bidIndex in range(len(bids)):
            bidsPrice.append(bids[bidIndex].price)

        bidsStackCopy = {}
        for bidPriceIndex in range(len(bidsPrice)):
            price = bidsPrice[bidPriceIndex]
            if price in self.bidsStack:
                bidsStackCopy.update({price: self.bidsStack[price]})

        bidsStack = dict(bidsStackCopy)
        for bidIndex in range(len(bids)):
            bid = bids[bidIndex]
            bidStack = self.bidsStack.get(bid.price)
            change = 0

            if bidStack:
                change = 100 * (int(bid.quantity) -
                                bidStack.get('value')) / bidStack.get('value')
                ratio = 100 * int(bid.quantity) / self.amountOffersAndBids
                maxValue = int(bid.quantity) if int(bid.quantity) > bidStack.get(
                    'maxValue') else bidStack.get('maxValue')
                inserter = {}
                inserterChild = {
                    'value': int(bid.quantity),
                    'prevValue': int(bidStack.get('value')),
                    'maxValue': maxValue,
                    'change': change,
                    'ratio': ratio,
                    'tradesQty': int(bidStack.get('tradesQty'))
                }
                inserter[bid.price] = inserterChild
                bidsStack.update(inserter)
            else:
                ratio = 100 * int(bid.quantity) / self.amountOffersAndBids
                bidsStack.update(
                    {bid.price: {'value': int(bid.quantity), 'change': 0, 'ratio': ratio, 'maxValue': int(bid.quantity), 'tradesQty': 0}})
        self.bidsStackLevelII = bidsStack.copy()
        self.bidsStack = bidsStack.copy()
        print 'change bid ---'
        for key in sorted(bidsStack, reverse=True):
            print "%s: %s" % (key, bidsStack[key])

    def updateOfferSide(self, trade):
        """ Обновляет значение прошедшего объема в уровень """
        price = str(Decimal(trade.price).quantize(Decimal("1.00")))
        offer = self.offersStack.get(price)
        if offer:
            offer['tradesQty'] = offer.get('tradesQty', 0) + int(trade.qty)
            self.offersStack.update({price: offer})

    def updateBidSide(self, trade):
        """ Обновляет значение прошедшего объема в уровень """
        price = str(Decimal(trade.price).quantize(Decimal("1.00")))
        bid = self.bidsStack.get(price)
        if bid:
            bid['tradesQty'] = bid.get('tradesQty', 0) + int(trade.qty)
            self.bidsStack.update({price: bid})


if __name__ == '__main__':
    Connector().subscribeQuoteLevelIIWithAllTrades()

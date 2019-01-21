# -*- coding: utf-8 -*-

# 1. subscribe to 7
# 2. createDataSource

import os, sys, time, signal, zmq

from decimal import Decimal
from request import Request

sys.path.insert(0, './api')

class AllTrades(Request):

    ctx = zmq.Context.instance()

    client = ctx.socket(zmq.REQ)
    client.connect('tcp://127.0.0.1:5560')

    __uuid = None
    lastPrice = None

    ordersShortStack = {}
    ordersLongStack = {}

    orderMinuteVolume = {}
    minuteVolumeLong = {}
    minuteVolumeShort = {}

    halfMinuteVolumeLong = {}
    halfMinuteVolumeShort = {}

    averageOrderValue = []

    def clear(self): 
        return os.system('cls')

    def current_milli_time(self): 
        return int(round(time.time() * 1000))

    def getDataSource(self, cb=None):
        """ Запрашивает источник """
        client = self.ctx.socket(zmq.REQ)
        client.connect('tcp://127.0.0.1:5560')

        request = self.fetchDataSourceTrade()
        client.send(request)
        message = client.recv()
        self.__uuid = self.parseDataSourceTrade(message)

        requestEmptyCallback = self.setEmptyCallbackTrade(self.__uuid)
        client.send(requestEmptyCallback)
        responseEmptyCallback = client.recv()
        isAwaitCallback = self.parseEmptyCallbackTrade(responseEmptyCallback)
        # print 'isAwaitCallback ', isAwaitCallback

        self.getDataSourceSize()
        self.subscribeOnAllTrades(cb)


    def subscribeOnAllTrades(self, cb=None):
        socket = self.ctx.socket(zmq.SUB)
        socket.connect('tcp://127.0.0.1:5561')
        socket.subscribe('7')

        should_continue = True
        while should_continue:
            messageNumber = socket.recv()
            messageResult = socket.recv()
            # print 'message ', messageNumber
            # print 'messageResult ', messageResult
            trade = self.parseAllTrades(messageResult)

            self.volume(trade)
            if trade.flags == 1:
                self.setMinuteVolumeShort(trade)
                self.calculateMinuteSliceVolumeShort(trade)
                self.shortTrade(trade)
            else:
                self.setMinuteVolumeLong(trade)
                self.calculateMinuteSliceVolumeLong(trade)
                self.longTrade(trade)

            if cb:
                cb(trade)


    def getDataSourceSize(self):
        request = self.fetchDataSourceSizeTrade(self.__uuid)
        self.client.send(request)
        message = self.client.recv()
        self.parseDataSourceSizeTrade(message)


    def shortTrade(self, trade):
        """ Собирает принты на шорт, чтобы высчитывать ускорение """
        self.averageOrderValue.append(trade.qty)
        averageQty = sum(map(lambda qty: qty, self.averageOrderValue)
                        ) / len(self.averageOrderValue)

        ms = int(round(time.time() * 1000))
        orderList = self.ordersShortStack.get(trade.price)
        if orderList:
            orderList.append({'time': ms, 'qty': trade.qty})

            amountQty = sum(map(lambda order: order.get('qty'), orderList))
            deltaTime = ms - orderList[0].get('time')
            deltaTime = deltaTime if deltaTime != 0 else 0.1
            intensiveQty = Decimal(amountQty / float(deltaTime))
            intensiveQty = intensiveQty.quantize(Decimal("1.00"))
            intensiveHit = Decimal(len(orderList) / float(deltaTime))
            intensiveHit = intensiveHit.quantize(Decimal("1.00"))

            averageSize = Decimal(amountQty / float(len(orderList)))
            averageSize = averageSize.quantize(Decimal("1.00"))
            # print 'Intense Short ', trade.price, ' - ', intensiveQty, ' - ', intensiveHit
            # print 'Sh ', trade.price, ' a:', amountQty, ' as:', averageSize, self.volumeByTrade(
                # trade)

            self.ordersShortStack = {trade.price: orderList}
        else:
            self.ordersShortStack.update(
                {trade.price: [{'time': ms, 'qty': trade.qty}]})


    def longTrade(self, trade):
        """ Собирает принты на лонг, чтобы высчитывать ускорение """
        self.averageOrderValue.append(trade.qty)
        averageQty = sum(map(lambda qty: qty, self.averageOrderValue)
                        ) / len(self.averageOrderValue)

        ms = int(round(time.time() * 1000))
        orderList = self.ordersLongStack.get(trade.price)
        if orderList:
            orderList.append({'time': ms, 'qty': trade.qty})

            amountQty = sum(map(lambda order: order.get('qty'), orderList))
            deltaTime = ms - orderList[0].get('time')
            deltaTime = deltaTime if deltaTime != 0 else 0.1
            intensiveQty = Decimal(amountQty / float(deltaTime))
            intensiveQty = intensiveQty.quantize(Decimal("1.00"))
            intensiveHit = Decimal(len(orderList) / float(deltaTime))
            intensiveHit = intensiveHit.quantize(Decimal("1.00"))

            averageSize = Decimal(amountQty / float(len(orderList)))
            averageSize = averageSize.quantize(Decimal("1.00"))
            # print 'Intense Long ', trade.price, ' - ', intensiveQty, ' - ', intensiveHit
            # print 'Lo ', trade.price, ' a:', amountQty, ' as:', averageSize, self.volumeByTrade(
                # trade)

            self.ordersLongStack = {trade.price: orderList}
        else:
            self.ordersLongStack.update({trade.price: [{'time': ms, 'qty': trade.qty}]})


    def setMinuteVolumeLong(self, trade):
        """ Считает объем в лонг по минутам """
        timeKey = str(trade.datetime.hour) + ':' + str(trade.datetime.min)
        minuteVolume = self.minuteVolumeLong.get(timeKey)
        if minuteVolume:
            self.minuteVolumeLong.update({timeKey: minuteVolume + int(trade.qty)})
        else:
            self.minuteVolumeLong.update({timeKey: trade.qty})


    def calculateMinuteSliceVolumeLong(self, trade):
        """ Считает объем в лонг по 30 секундам """
        half = '00' if trade.datetime.sec < 30 else '30'
        timeKey = str(trade.datetime.hour) + ':' + \
            str(trade.datetime.min) + ':' + half
        minuteVolume = self.halfMinuteVolumeLong.get(timeKey)
        if minuteVolume:
            self.halfMinuteVolumeLong.update({timeKey: minuteVolume + int(trade.qty)})
        else:
            self.halfMinuteVolumeLong.update({timeKey: trade.qty})


    def calculateMinuteSliceVolumeShort(self, trade):
        """ Считает объем в шорт по 30 секундам """
        half = '00' if trade.datetime.sec < 30 else '30'
        timeKey = str(trade.datetime.hour) + ':' + \
            str(trade.datetime.min) + ':' + half
        minuteVolume = self.halfMinuteVolumeShort.get(timeKey)
        if minuteVolume:
            self.halfMinuteVolumeShort.update({timeKey: minuteVolume + int(trade.qty)})
        else:
            self.halfMinuteVolumeShort.update({timeKey: trade.qty})


    def setMinuteVolumeShort(self, trade):
        """ Считает объем в шорт по минутам """
        timeKey = str(trade.datetime.hour) + ':' + str(trade.datetime.min)
        minuteVolume = self.minuteVolumeShort.get(timeKey)
        if minuteVolume:
            self.minuteVolumeShort.update({timeKey: minuteVolume + int(trade.qty)})
        else:
            self.minuteVolumeShort.update({timeKey: trade.qty})


    def volume(self, trade):
        """ Считает объем по минутам """
        timeKey = str(trade.datetime.hour) + ':' + str(trade.datetime.min)
        minuteVolume = self.orderMinuteVolume.get(timeKey)
        if minuteVolume:
            self.orderMinuteVolume.update({timeKey: minuteVolume + int(trade.qty)})
        else:
            self.orderMinuteVolume.update({timeKey: trade.qty})

        return self.orderMinuteVolume.get(timeKey)


    def volumeByTrade(self, trade):
        """ отдает объем по минутам """
        half = '00' if trade.datetime.sec < 30 else '30'
        halfTimeKey = str(trade.datetime.hour) + ':' + \
            str(trade.datetime.min) + ':' + half

        timeKey = str(trade.datetime.hour) + ':' + str(trade.datetime.min)
        return trade.datetime.sec,  self.orderMinuteVolume.get(timeKey), self.minuteVolumeLong.get(timeKey), self.minuteVolumeShort.get(timeKey), self.halfMinuteVolumeLong.get(halfTimeKey), self.halfMinuteVolumeShort.get(halfTimeKey)


    def exitScript(self, signum, frame):
        requestClose = self.fetchDataSourceCloseSourceTrade(self.__uuid)
        self.client.send(requestClose)
        message = self.client.recv()
        self.parseDataSourceCloseTrade(message)
        sys.exit(1)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, AllTrades.exitScript)
    AllTrades().getDataSource()

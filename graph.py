# -*- coding: utf-8 -*-

import os
import zmq
import time

from decimal import Decimal
from request import Request

class Graph(Request):
    ctx = zmq.Context.instance()

    def __init__(self):
        self.maxHeightsGraph = None
        self.minLowsGraph = None
        self.averageQtyGraph = None
        self.averageCandleBodyGraph = None
        self.averageImpulseLengthGraph = None
        self.averageImpulseVolumeGraph = None
        self.isImpulseGraph = None
        self.impulseBodyGraph = None
        self.impulseAmountVolumeGraph = None

    def clear(self): return os.system('cls')

    def maxHeightList(self, candleHeights):
        # Находит максимумы и наибольшее количество попаданий на одинаковый максимум
        maxHeights = []
        candleLength = len(candleHeights)
        step = 3
        for mainHighIndex in range(step, candleLength-step):
            mainHeight = float(candleHeights[mainHighIndex])
            isLeftLess = True
            isRightLess = True

            for leftIndex in range(mainHighIndex-step, mainHighIndex):
                leftCandle = float(candleHeights[leftIndex])
                if leftCandle > mainHeight:
                    isLeftLess = False
            for rightIndex in range(mainHighIndex, mainHighIndex+step):
                rightCandle = float(candleHeights[rightIndex])
                if rightCandle > mainHeight:
                    isRightLess = False

            if isLeftLess and isRightLess:
                maxHeights.append(mainHeight)

        counterHighTimes = {}
        for high in range(len(maxHeights)):
            highValue = maxHeights[high]
            counterByHigh = counterHighTimes.get(highValue, 0)
            if not counterByHigh:
                counterHighTimes.update({highValue: 1})
            else:
                inserter = {}
                inserter[highValue] = counterByHigh + 1
                counterHighTimes.update(inserter)

        self.maxHeightsGraph = maxHeights
        print 'maxHeights ', maxHeights[-3:]


    def minLowList(self, candleLows):
        # Находит минимумы
        minLows = []
        candleLength = len(candleLows)
        step = 3

        for mainLowIndex in range(step, candleLength-step):
            mainLow = float(candleLows[mainLowIndex])
            isLeftMore = True
            isRightMore = True

            for leftIndex in range(mainLowIndex-step, mainLowIndex):
                leftCandle = float(candleLows[leftIndex])
                if leftCandle < mainLow:
                    isLeftMore = False

            for rightIndex in range(mainLowIndex, mainLowIndex+step):
                rightCandle = float(candleLows[rightIndex])
                if rightCandle < mainLow:
                    isRightMore = False

            if isLeftMore and isRightMore:
                minLows.append(mainLow)

        self.minLowsGraph = minLows
        print 'minLows ', minLows[-3:]


    def averageVolume(self, candleVolumes):
        averageQty = sum(map(lambda qty: qty, candleVolumes)) / len(candleVolumes)
        self.averageQtyGraph = averageQty
        print 'minute - averageQty ', averageQty


    def averageCandleBody(self, candleHeights, candleLows, candleLength):
        """ Высчитывает среднее тело 1 минутной свечи """
        candlesHighLow = []
        for index in range(0, candleLength - 1):
            candlesHighLow.append(
                {'high': float(candleHeights[index]), 'low': float(candleLows[index])})

        candleBodies = []
        for index in range(0, len(candlesHighLow)):
            candleBodies.append(candlesHighLow[index].get(
                'high') - candlesHighLow[index].get('low'))

        averageCandleBody = sum(
            map(lambda body: body, candleBodies)) / len(candleBodies)
        averageCandleBody = Decimal(averageCandleBody)
        averageCandleBody = averageCandleBody.quantize(Decimal("1.00"))

        self.averageCandleBodyGraph = averageCandleBody
        print 'minute - averageCandleBody ', averageCandleBody

    def detectImpulse(self, candleHeights, candleLows, candleOpens, candleCloses, candleTimes, candleVolumes, candleLength):
        """ Находит импульсы и считает данные по ним """
        isImpulse = False

        directions = []
        for index in range(candleLength-1):
            candleOpen = candleOpens[index]
            candleClose = candleCloses[index]
            diff = float(candleClose) - float(candleOpen)

            if diff > 0:
                direction = 'up'
            elif diff < 0:
                direction = 'down'
            else:
                direction = 'None'

            directions.append(direction)

        directionImpulses = []
        for index in range(len(directions)):
            direction = directions[index]
            countInRow = 1
            for subIndex in range(index+1, len(directions)):
                nextDirection = directions[subIndex]
                if nextDirection == direction:
                    countInRow += 1
                else:
                    break
            inserter = {
                'direction': direction,
                'count': countInRow
            }
            directionImpulses.append(inserter)

        skipStep = 0
        for index in range(len(directionImpulses)):
            body = 0
            amountVolume = 0

            direction = directionImpulses[index]
            count = direction.get('count')
            directionType = direction.get('direction')

            time = candleTimes[index]

            if skipStep > 0:
                skipStep -= 1
                continue

            if count >= 2:
                impulseCandleLength = index + count
                for candleIndex in range(index, impulseCandleLength):
                    candleOpen = candleOpens[candleIndex]
                    candleClose = candleCloses[candleIndex]
                    volume = candleVolumes[candleIndex]
                    candleBody = 0
                    if directionType == 'up':
                        candleBody = float(candleClose) - float(candleOpen)
                    elif directionType == 'down':
                        candleBody = float(candleOpen) - float(candleClose)
                    candleBody = Decimal(candleBody)
                    candleBody = candleBody.quantize(Decimal("1.00"))
                    body += candleBody
                    amountVolume += volume
                    directionImpulses[candleIndex].update({ 'isImpulse': True })

                skipStep = count
                inserter = {
                    'direction': directionType,
                    'count': count,
                    'impulseLength': body,
                    'impulseVolume': amountVolume,
                    'isImpulse' : True,
                    'time': str(time.hour) + ':' + str(time.min)
                }
                directionImpulses[index] = inserter

        impulseLengths = []
        for index in range(len(directionImpulses)):
            directionImpulse = directionImpulses[index]
            impulseLength = directionImpulse.get('impulseLength')
            if impulseLength:
                impulseLengths.append(impulseLength)

        impulseVolumes = []
        for index in range(len(directionImpulses)):
            directionImpulse = directionImpulses[index]
            impulseVolume = directionImpulse.get('impulseVolume')
            if impulseVolume:
                impulseVolumes.append(impulseVolume)
        
        averageImpulseLength = sum(map(lambda impulseLength: impulseLength, impulseLengths)) / len(impulseLengths)
        averageImpulseLength = Decimal(averageImpulseLength)
        averageImpulseLength = averageImpulseLength.quantize(Decimal("1.00"))
        self.averageImpulseLengthGraph = averageImpulseLength
        print 'averageImpulseLength ', averageImpulseLength

        averageImpulseVolume = sum(map(lambda impulseVolume: impulseVolume, impulseVolumes)) / len(impulseVolumes)
        averageImpulseVolume = Decimal(averageImpulseVolume)
        averageImpulseVolume = averageImpulseVolume.quantize(Decimal("1.00"))
        self.averageImpulseVolumeGraph = averageImpulseVolume
        print 'averageImpulseVolume ', averageImpulseVolume

        isImpulse = directionImpulses[len(directionImpulses)-1].get('isImpulse')
        self.isImpulseGraph = isImpulse
        print 'isImpulse', isImpulse

        if isImpulse:
            impulseStartIndex = None
            for index in reversed(range(len(directionImpulses))):
                directionImpulse = directionImpulses[index]
                time = directionImpulse.get('time')
                if time:
                    impulseStartIndex = index
                    break

            impulseBody = 0
            impulseAmountVolume = 0
            for index in range(impulseStartIndex, len(directionImpulses)):
                direction = directionImpulses[index]
                directionType = direction.get('direction')

                candleOpen = candleOpens[candleIndex]
                candleClose = candleCloses[candleIndex]
                volume = candleVolumes[candleIndex]
                candleBody = 0
                if directionType == 'up':
                    candleBody = float(candleClose) - float(candleOpen)
                elif directionType == 'down':
                    candleBody = float(candleOpen) - float(candleClose)

                candleBody = Decimal(candleBody)
                candleBody = candleBody.quantize(Decimal("1.00"))
                impulseBody += candleBody
                impulseAmountVolume += volume
            
            self.impulseBodyGraph = impulseBody
            self.impulseAmountVolumeGraph = impulseAmountVolume
            print 'impulseBody ', impulseBody
            print 'impulseAmountVolume ', impulseAmountVolume


    def base(self, client, uuid, cb):
        requestDataSourceSize = self.fetchDataSourceSizeGraph(uuid)
        client.send(requestDataSourceSize)
        responseDataSourceSize = client.recv()
        candleLength = self.parseDataSourceSizeGraph(responseDataSourceSize)
        if candleLength:
            candleLength += 1
        print 'candleLength ', candleLength

        candleHeights = []
        for index in range(0, candleLength):
            requestCandleHeight = self.fetchDataSourceHeightGraph(uuid, index)
            client.send(requestCandleHeight)
            responseCandleHeight = client.recv()
            candleHeight = self.parseDataSourceHeightGraph(responseCandleHeight)
            candleHeights.append(candleHeight)

        candleLows = []
        for index in range(0, candleLength):
            requestCandleLow = self.fetchDataSourceLowGraph(uuid, index)
            client.send(requestCandleLow)
            responseCandleLow = client.recv()
            candleLow = self.parseDataSourceLowGraph(responseCandleLow)
            candleLows.append(candleLow)

        candleOpens = []
        for index in range(0, candleLength):
            requestCandleOpen = self.fetchDataSourceOpenGraph(uuid, index)
            client.send(requestCandleOpen)
            responseCandleOpen = client.recv()
            candleOpen = self.parseDataSourceOpenGraph(responseCandleOpen)
            candleOpens.append(candleOpen)

        candleCloses = []
        for index in range(0, candleLength):
            requestCandleClose = self.fetchDataSourceCloseGraph(uuid, index)
            client.send(requestCandleClose)
            responseCandleClose = client.recv()
            candleClose = self.parseDataSourceCloseGraph(responseCandleClose)
            candleCloses.append(float(candleClose))

        candleVolumes = []
        for index in range(0, candleLength):
            requestCandleVolume = self.fetchDataSourceVolumeGraph(uuid, index)
            client.send(requestCandleVolume)
            responseCandleVolume = client.recv()
            candleVolume = self.parseDataSourceVolumeGraph(responseCandleVolume)
            candleVolumes.append(int(candleVolume))

        candleTimes = []
        for index in range(0, candleLength):
            requestCandleTime = self.fetchDataSourceTimeGraph(uuid, index)
            client.send(requestCandleTime)
            responseCandleTime = client.recv()
            candleTime = self.parseDataSourceTimeGraph(responseCandleTime)
            candleTimes.append(candleTime)

        self.clear()
        self.maxHeightList(candleHeights)
        self.minLowList(candleLows)
        self.averageVolume(candleVolumes)
        self.averageCandleBody(candleHeights, candleLows, candleLength)
        self.detectImpulse(candleHeights, candleLows, candleOpens, candleCloses, candleTimes, candleVolumes, candleLength)

        if cb:
            cb()

        requestEmptyCallback = self.setEmptyCallbackGraph(uuid)
        client.send(requestEmptyCallback)
        responseEmptyCallback = client.recv()
        isAwaitCallback = self.parseEmptyCallbackGraph(responseEmptyCallback)
        
        if isAwaitCallback:
            self.base(client, uuid, cb)
        else:
            return isAwaitCallback


    def getData(self, cb=None):
        client = self.ctx.socket(zmq.REQ)
        client.connect('tcp://127.0.0.1:5560')

        requestDataSource = self.fetchDataSourceGraph()
        client.send(requestDataSource)
        responseDataSource = client.recv()
        uuid = self.parseDataSourceGraph(responseDataSource)

        self.base(client, uuid, cb)

        requestClose = self.fetchDataSourceCloseSourceGraph(uuid)
        client.send(requestClose)
        responseClose = client.recv()
        isClosed = self.parseDataSourceCloseSourceGraph(responseClose)
        print 'isClosed ', isClosed

if __name__ == '__main__':
    Graph().getData()
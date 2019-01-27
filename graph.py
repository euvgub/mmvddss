# -*- coding: utf-8 -*-

import os
import time
import math
import zmq

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

    def maxHeightList(self, candleHeights, candleCloses):
        # Находит максимумы и наибольшее количество попаданий на одинаковый максимум
        maxHeights = []
        candleLength = len(candleHeights)
        step = 3

        for mainHighIndex in range(step, candleLength-step):
            mainHeight = float(candleHeights[mainHighIndex])
            isLeftLess = True
            isRightLess = True
            isLeftEqual = False
            isRightEqual = False

            for leftIndex in range(mainHighIndex-step, mainHighIndex):
                leftCandle = float(candleHeights[leftIndex])
                if leftCandle > mainHeight:
                    isLeftLess = False
                elif leftCandle == mainHeight:
                    isLeftEqual = True

            for rightIndex in range(mainHighIndex + 1, mainHighIndex+step):
                rightCandle = float(candleHeights[rightIndex])
                if rightCandle > mainHeight:
                    isRightLess = False
                elif rightCandle == mainHeight:
                    isRightEqual = True

            if isLeftLess and isRightLess and isLeftEqual and not isRightEqual:
                maxHeights.append(
                    {'price': mainHeight, 'index': mainHighIndex})
                continue

            if isLeftLess and isRightLess and not isLeftEqual and not isRightEqual:
                maxHeights.append(
                    {'price': mainHeight, 'index': mainHighIndex})
                continue

        # counterHighTimes = {}
        # for high in range(len(maxHeights)):
        #     highValue = maxHeights[high]
        #     counterByHigh = counterHighTimes.get(highValue, 0)
        #     if not counterByHigh:
        #         counterHighTimes.update({highValue: 1})
        #     else:
        #         inserter = {}
        #         inserter[highValue] = counterByHigh + 1
        #         counterHighTimes.update(inserter)

        self.maxHeightsGraph = maxHeights
        # lastPrice = float(candleCloses[len(candleCloses)-1])
        # nearestHigh = list(filter(lambda x: float(x) >= lastPrice, maxHeights))
        # print 'nearestHigh ', nearestHigh[len(nearestHigh)-1]

    def minLowList(self, candleLows, candleCloses):
        # Находит минимумы
        minLows = []
        candleLength = len(candleLows)
        step = 3

        for mainLowIndex in range(step, candleLength - step):
            mainLow = float(candleLows[mainLowIndex])
            isLeftMore = True
            isRightMore = True
            isLeftEqual = False
            isRightEqual = False

            for leftIndex in range(mainLowIndex-step, mainLowIndex):
                leftCandle = float(candleLows[leftIndex])
                if leftCandle < mainLow:
                    isLeftMore = False
                elif leftCandle == mainLow:
                    isLeftEqual = True

            for rightIndex in range(mainLowIndex+1, mainLowIndex+step):
                rightCandle = float(candleLows[rightIndex])
                if rightCandle < mainLow:
                    isRightMore = False
                elif rightCandle == mainLow:
                    isRightEqual = True

            if isLeftMore and isRightMore and isLeftEqual and not isRightEqual:
                minLows.append({'price': mainLow, 'index': mainLowIndex})
                continue

            if isLeftMore and isRightMore and not isLeftEqual and not isRightEqual:
                minLows.append({'price': mainLow, 'index': mainLowIndex})
                continue

        self.minLowsGraph = minLows
        # lastPrice = float(candleCloses[len(candleCloses)-1])
        # nearestLow = list(filter(lambda x: float(x) <= lastPrice, minLows))
        # print 'len(nearestLow)', len(nearestLow)
        # print 'nearestLow ', nearestLow[len(nearestLow)-1]

    def averageVolume(self, candleVolumes):
        averageQty = sum(map(lambda qty: qty, candleVolumes)
                         ) / len(candleVolumes)
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
                    directionImpulses[candleIndex].update({'isImpulse': True})

                skipStep = count
                inserter = {
                    'direction': directionType,
                    'count': count,
                    'impulseLength': body,
                    'impulseVolume': amountVolume,
                    'isImpulse': True,
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

        averageImpulseLength = sum(
            map(lambda impulseLength: impulseLength, impulseLengths)) / len(impulseLengths)
        averageImpulseLength = Decimal(averageImpulseLength)
        averageImpulseLength = averageImpulseLength.quantize(Decimal("1.00"))
        self.averageImpulseLengthGraph = averageImpulseLength
        print 'averageImpulseLength ', averageImpulseLength

        averageImpulseVolume = sum(
            map(lambda impulseVolume: impulseVolume, impulseVolumes)) / len(impulseVolumes)
        averageImpulseVolume = Decimal(averageImpulseVolume)
        averageImpulseVolume = averageImpulseVolume.quantize(Decimal("1.00"))
        self.averageImpulseVolumeGraph = averageImpulseVolume
        print 'averageImpulseVolume ', averageImpulseVolume

        isImpulse = directionImpulses[len(
            directionImpulses)-1].get('isImpulse')
        impulseDirection = directionImpulses[len(
            directionImpulses)-1].get('direction')
        self.isImpulseGraph = isImpulse
        print 'isImpulse', isImpulse
        if isImpulse:
            print 'impulseDirection ', impulseDirection

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

                candleOpen = candleOpens[index]
                candleClose = candleCloses[index]
                volume = candleVolumes[index]
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
            candleHeight = self.parseDataSourceHeightGraph(
                responseCandleHeight)
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
            candleVolume = self.parseDataSourceVolumeGraph(
                responseCandleVolume)
            candleVolumes.append(int(candleVolume))

        candleTimes = []
        for index in range(0, candleLength):
            requestCandleTime = self.fetchDataSourceTimeGraph(uuid, index)
            client.send(requestCandleTime)
            responseCandleTime = client.recv()
            candleTime = self.parseDataSourceTimeGraph(responseCandleTime)
            candleTimes.append(candleTime)

        self.clear()
        self.maxHeightList(candleHeights, candleCloses)
        self.minLowList(candleLows, candleCloses)
        self.averageVolume(candleVolumes)
        self.averageCandleBody(candleHeights, candleLows, candleLength)
        self.detectImpulse(candleHeights, candleLows, candleOpens,
                           candleCloses, candleTimes, candleVolumes, candleLength)
        self.__TechnicalAnalyzeDetect(candleCloses)

        if cb:
            cb()

        requestEmptyCallback = self.setEmptyCallbackGraph(uuid)
        client.send(requestEmptyCallback)
        responseEmptyCallback = client.recv()
        isAwaitCallback = self.parseEmptyCallbackGraph(responseEmptyCallback)

        if isAwaitCallback:
            # time.sleep(60)
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

    def __findMinValue(self, priceList):
        lowPrice = 0
        for priceObject in priceList:
            price = priceObject.get('price')
            if lowPrice == 0:
                lowPrice = price
            if price > lowPrice:
                continue
            else:
                lowPrice = price

        return lowPrice

    def __findMaxValue(self, priceList):
        highPrice = 0
        for priceObject in priceList:
            price = priceObject.get('price')
            if highPrice == 0:
                highPrice = price
            if price < highPrice:
                continue
            else:
                highPrice = price

        return highPrice

    def __drawLine(self, x1=0, y1=0, x2=0, y2=0):
        dy = y2 - y1
        dx = x2 - x1
        dx = dx if dx != 0 else 1
        k = float(dy)/float(dx)
        return k

    def __findPriceByRadian(self, x1=0, y1=0, x2=0, k=0):
        dx = x2 - x1
        dk = float(dx) * float(k)
        y2 = dk + float(y1)
        return float(math.floor(y2) / 100)

    def __TechnicalAnalyzeDetect(self, candleCloses):
        highLineType = None
        lowLineType = None

        lastPrice = float(candleCloses[len(candleCloses)-1])
        lastIndex = len(candleCloses) - 1

        lows = list()
        for index in range(len(self.minLowsGraph)):
            low = self.minLowsGraph[index]
            price = low.get('price')
            lowIndex = low.get('index')
            if price - 0.02 <= lastPrice:
                lows.append({'price': price, 'index': lowIndex})

        highs = list()
        for index in range(len(self.maxHeightsGraph)):
            high = self.maxHeightsGraph[index]
            price = high.get('price')
            highIndex = high.get('index')
            if price + 0.02 >= lastPrice:
                highs.append({'price': price, 'index': highIndex})

        availableHighs = list()
        for index in reversed(range(len(highs))):
            high = highs[index]
            highPrice = high.get('price')
            highIndex = high.get('index')
            maxPrice = price if len(
                availableHighs) == 0 else self.__findMaxValue(availableHighs)
            if maxPrice <= highPrice + 0.05:
                availableHighs.append({'price': highPrice, 'index': highIndex})
        availableHighs.reverse()

        availableLows = list()
        for index in reversed(range(len(lows))):
            low = lows[index]
            lowPrice = low.get('price')
            lowIndex = low.get('index')
            minPrice = lowPrice if len(
                availableLows) == 0 else self.__findMinValue(availableLows)
            if minPrice >= lowPrice - 0.05:
                availableLows.append({'price': lowPrice, 'index': lowIndex})
        availableLows.reverse()

        print 'availableHighs ', availableHighs
        print 'availableLows ', availableLows

        counterHigh = list()
        direction = None
        for index in reversed(range(len(availableHighs))):
            prevHigh = availableHighs[index - 1]
            prevHighPrice = prevHigh.get('price')
            prevHighIndex = prevHigh.get('index')
            currentHigh = availableHighs[index]
            currentHighPrice = currentHigh.get('price')
            currentHighIndex = currentHigh.get('index')

            localDirection = currentHighPrice - prevHighPrice
            if localDirection <= 0.05 and localDirection >= -0.05:
                if direction and direction != 'equal':
                    if localDirection > 0:
                        localDirection = 'up'
                    elif localDirection < 0:
                        localDirection = 'down'
                else:
                    localDirection = 'equal'
            elif localDirection > 0:
                localDirection = 'up'
            elif localDirection < 0:
                localDirection = 'down'

            if not direction:
                direction = localDirection
                counterHigh.append(
                    {'price': currentHighPrice, 'index': currentHighIndex})
            elif direction == localDirection:
                counterHigh.append(
                    {'price': currentHighPrice, 'index': currentHighIndex})
            else:
                if len(counterHigh) == 1:
                    counterHigh.append(
                        {'price': currentHighPrice, 'index': currentHighIndex})
                break

        if len(counterHigh):
            counterHigh.reverse()
            print '---------'
            for index in range(len(counterHigh) - 1):
                highA = counterHigh[index]
                highB = counterHigh[index + 1]

                highAx = highA.get('index')
                highAy = highA.get('price') * 100

                highBx = highB.get('index')
                highBy = highB.get('price') * 100
                corner = self.__drawLine(highAx, highAy, highBx, highBy)

                expectationPrice = self.__findPriceByRadian(
                    highAx, highAy, lastIndex, corner)
                if expectationPrice >= lastPrice:
                    print 'need price High', expectationPrice

            # print 'corner position by high', self.__drawLine(counterHigh[0].get(
            #     'index'), counterHigh[0].get('price') * 100, lastIndex, lastPrice * 100)
            # counterHigh.reverse()
            if direction == 'equal':
                highLineType = 'horizontal'
            elif direction == 'up':
                highLineType = 'increase'
            else:
                highLineType = 'decrease'

        counterLow = list()
        direction = None
        for index in reversed(range(len(availableLows))):
            prevLow = availableLows[index - 1]
            prevLowPrice = prevLow.get('price')
            prevLowIndex = prevLow.get('index')
            currentLow = availableLows[index]
            currentLowPrice = currentLow.get('price')
            currentLowIndex = currentLow.get('index')

            localDirection = currentLowPrice - prevLowPrice
            if localDirection <= 0.05 and localDirection >= -0.05:
                if direction and direction != 'equal':
                    if localDirection > 0:
                        localDirection = 'down'
                    elif localDirection < 0:
                        localDirection = 'up'
                else:
                    localDirection = 'equal'
            elif localDirection > 0:
                localDirection = 'down'
            elif localDirection < 0:
                localDirection = 'up'

            if not direction:
                direction = localDirection
                counterLow.append(
                    {'price': currentLowPrice, 'index': currentLowIndex})
            elif direction == localDirection:
                counterLow.append(
                    {'price': currentLowPrice, 'index': currentLowIndex})
            else:
                if len(counterLow) != 0:
                    counterLow.append(
                        {'price': currentLowPrice, 'index': currentLowIndex})
                break

        if len(counterLow):
            counterLow.reverse()
            print '---------'
            for index in range(len(counterLow) - 1):
                lowA = counterLow[index]
                lowB = counterLow[index + 1]

                lowAx = lowA.get('index')
                lowAy = lowA.get('price') * 100

                lowBx = lowB.get('index')
                lowBy = lowB.get('price') * 100
                corner = self.__drawLine(lowAx, lowAy, lowBx, lowBy)

                expectationPrice = self.__findPriceByRadian(
                    lowAx, lowAy, lastIndex, corner)
                if expectationPrice <= lastPrice:
                    print 'need price Low', expectationPrice

            # print 'corner position by low', self.__drawLine(counterLow[0].get(
            #     'index'), counterLow[0].get('price') * 100, lastIndex, lastPrice * 100)

            # counterLow.reverse()
            if direction == 'equal':
                lowLineType = 'horizontal'
            elif direction == 'down':
                lowLineType = 'increase'
            else:
                lowLineType = 'decrease'

        print '---------'
        # print 'availableHighs ', self.maxHeightsGraph
        # print 'availableLows ', self.minLowsGraph
        print 'highLineType ', highLineType, ' - ', counterHigh
        print 'lowLineType ', lowLineType, ' - ', counterLow


if __name__ == '__main__':
    Graph().getData()

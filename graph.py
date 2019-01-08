# -*- coding: utf-8 -*-

import os
import sys
import zmq
import time
from decimal import Decimal

from api.qlua import RPC_pb2
from api.qlua import qlua_structures_pb2
from api.qlua.datasource import CreateDataSource_pb2
from api.qlua.datasource import Size_pb2
from api.qlua.datasource import Close_pb2
from api.qlua.datasource import H_pb2
from api.qlua.datasource import L_pb2
from api.qlua.datasource import O_pb2
from api.qlua.datasource import C_pb2
from api.qlua.datasource import V_pb2
from api.qlua.datasource import T_pb2
from api.qlua.datasource import SetEmptyCallback_pb2

sys.path.insert(0, './api')


def clear(): return os.system('cls')


ctx = zmq.Context.instance()


# Запрашивает создание источника данных для свечек
def fetchDataSource():
    message = CreateDataSource_pb2.Request()
    message.class_code = 'QJSIM'
    message.sec_code = 'SBER'
    message.interval = CreateDataSource_pb2.INTERVAL_M1

    request = RPC_pb2.Request()
    request.type = RPC_pb2.CREATE_DATA_SOURCE
    request.args = message.SerializeToString()
    print "Request ", request
    return request.SerializeToString()


# Парсит создание источника данных для свечек, вытаскивает uuid в терминале для этого источника
def parseDataSource(message):
    response = RPC_pb2.Response()
    response.ParseFromString(message)
    messageResult = CreateDataSource_pb2.Result()
    messageResult.ParseFromString(response.result)
    print "Response ", messageResult
    return messageResult.datasource_uuid

# Отправляет запрос на закрытие источника


def fetchDataSourceCloseSource(uuid):
    message = Close_pb2.Request()
    message.datasource_uuid = uuid

    request = RPC_pb2.Request()
    request.type = RPC_pb2.DS_CLOSE
    request.args = message.SerializeToString()
    return request.SerializeToString()

# Парсит ответ на закрытие источника


def parseDataSourceCloseSource(message):
    response = RPC_pb2.Response()
    response.ParseFromString(message)
    messageResult = Close_pb2.Result()
    messageResult.ParseFromString(response.result)
    return messageResult.result


# Запрашивает по uuid источника количество отданных  с сервера свечей
def fetchDataSourceSize(uuid):
    message = Size_pb2.Request()
    message.datasource_uuid = uuid

    request = RPC_pb2.Request()
    request.type = RPC_pb2.DS_SIZE
    request.args = message.SerializeToString()
    return request.SerializeToString()


# Парсит количество отданных свечей
def parseDataSourceSize(message):
    response = RPC_pb2.Response()
    response.ParseFromString(message)
    messageResult = Size_pb2.Result()
    messageResult.ParseFromString(response.result)
    return messageResult.value


# Запрашивает высоту свечи в потоке и от индекса свечи
def fetchDataSourceHeight(uuid, index):
    message = H_pb2.Request()
    message.datasource_uuid = uuid
    message.candle_index = index

    request = RPC_pb2.Request()
    request.type = RPC_pb2.DS_H
    request.args = message.SerializeToString()
    return request.SerializeToString()


# Парсит высоту свечи
def parseDataSourceHeight(message):
    response = RPC_pb2.Response()
    response.ParseFromString(message)
    messageResult = H_pb2.Result()
    messageResult.ParseFromString(response.result)
    # print "Response ", messageResult.value
    return messageResult.value


def fetchDataSourceLow(uuid, index):
    # Запрашивает высоту свечи в потоке и от индекса свечи
    message = L_pb2.Request()
    message.datasource_uuid = uuid
    message.candle_index = index

    request = RPC_pb2.Request()
    request.type = RPC_pb2.DS_L
    request.args = message.SerializeToString()
    return request.SerializeToString()


def parseDataSourceLow(message):
    # Парсит высоту свечи
    response = RPC_pb2.Response()
    response.ParseFromString(message)
    messageResult = L_pb2.Result()
    messageResult.ParseFromString(response.result)
    # print "Response ", messageResult.value
    return messageResult.value


def fetchDataSourceOpen(uuid, index):
    """ Запрашивает открытие свечи в потоке и от индекса свечи """
    message = O_pb2.Request()
    message.datasource_uuid = uuid
    message.candle_index = index

    request = RPC_pb2.Request()
    request.type = RPC_pb2.DS_O
    request.args = message.SerializeToString()
    return request.SerializeToString()


def parseDataSourceOpen(message):
    """ Запрашивает открытие свечи в потоке и от индекса свечи """
    response = RPC_pb2.Response()
    response.ParseFromString(message)
    messageResult = O_pb2.Result()
    messageResult.ParseFromString(response.result)
    return messageResult.value

def fetchDataSourceClose(uuid, index):
    """ Запрашивает закрытие свечи в потоке и от индекса свечи """
    message = C_pb2.Request()
    message.datasource_uuid = uuid
    message.candle_index = index

    request = RPC_pb2.Request()
    request.type = RPC_pb2.DS_C
    request.args = message.SerializeToString()
    return request.SerializeToString()

def parseDataSourceClose(message):
    """ Запрашивает закрытие свечи в потоке и от индекса свечи """
    response = RPC_pb2.Response()
    response.ParseFromString(message)
    messageResult = C_pb2.Result()
    messageResult.ParseFromString(response.result)
    return messageResult.value

def fetchDataSourceTime(uuid, index):
    """ Запрашивает время свечи в потоке и от индекса свечи """
    message = T_pb2.Request()
    message.datasource_uuid = uuid
    message.candle_index = index

    request = RPC_pb2.Request()
    request.type = RPC_pb2.DS_T
    request.args = message.SerializeToString()
    return request.SerializeToString()

def parseDataSourceTime(message):
    """ Запрашивает время свечи в потоке и от индекса свечи """
    response = RPC_pb2.Response()
    response.ParseFromString(message)
    messageResult = T_pb2.Result()
    messageResult.ParseFromString(response.result)
    return messageResult

def fetchDataSourceVolume(uuid, index):
    # Запрашивает объем свечи в потоке и от индекса свечи
    message = V_pb2.Request()
    message.datasource_uuid = uuid
    message.candle_index = index

    request = RPC_pb2.Request()
    request.type = RPC_pb2.DS_V
    request.args = message.SerializeToString()
    return request.SerializeToString()


def parseDataSourceVolume(message):
    # Парсит объем свечи
    response = RPC_pb2.Response()
    response.ParseFromString(message)
    messageResult = V_pb2.Result()
    messageResult.ParseFromString(response.result)
    # print "Response ", messageResult.value
    return messageResult.value


def setEmptyCallback(uuid):
    # Ставит пустой колбек
    message = SetEmptyCallback_pb2.Request()
    message.datasource_uuid = uuid

    request = RPC_pb2.Request()
    request.type = RPC_pb2.DS_SET_EMPTY_CALLBACK
    request.args = message.SerializeToString()
    return request.SerializeToString()


def parseEmptyCallback(message):
    # Парсит ответ на пустой колбек
    response = RPC_pb2.Response()
    response.ParseFromString(message)
    messageResult = SetEmptyCallback_pb2.Result()
    messageResult.ParseFromString(response.result)
    return messageResult.result


def maxHeightList(candleHeights):
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

    print 'maxHeights ', maxHeights[-3:]


def minLowList(candleLows):
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

    print 'minLows ', minLows[-3:]


def averageVolume(candleVolumes):
    averageQty = sum(map(lambda qty: qty, candleVolumes)) / len(candleVolumes)
    print 'minute - averageQty ', averageQty


def averageCandleBody(candleHeights, candleLows, candleLength):
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

    print 'minute - averageCandleBody ', averageCandleBody

def detectImpulse(candleHeights, candleLows, candleOpens, candleCloses, candleTimes, candleVolumes, candleLength):
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
    print 'averageImpulseLength ', averageImpulseLength

    averageImpulseVolume = sum(map(lambda impulseVolume: impulseVolume, impulseVolumes)) / len(impulseVolumes)
    averageImpulseVolume = Decimal(averageImpulseVolume)
    averageImpulseVolume = averageImpulseVolume.quantize(Decimal("1.00"))
    print 'averageImpulseVolume ', averageImpulseVolume

    isImpulse = directionImpulses[len(directionImpulses)-1].get('isImpulse')
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
        
        print 'impulseBody ', impulseBody
        print 'impulseAmountVolume ', impulseAmountVolume


def base(client, uuid):
    requestDataSourceSize = fetchDataSourceSize(uuid)
    client.send(requestDataSourceSize)
    responseDataSourceSize = client.recv()
    candleLength = parseDataSourceSize(responseDataSourceSize)
    if candleLength:
        candleLength += 1
    print 'candleLength ', candleLength

    candleHeights = []
    for index in range(0, candleLength):
        requestCandleHeight = fetchDataSourceHeight(uuid, index)
        client.send(requestCandleHeight)
        responseCandleHeight = client.recv()
        candleHeight = parseDataSourceHeight(responseCandleHeight)
        candleHeights.append(candleHeight)

    candleLows = []
    for index in range(0, candleLength):
        requestCandleLow = fetchDataSourceLow(uuid, index)
        client.send(requestCandleLow)
        responseCandleLow = client.recv()
        candleLow = parseDataSourceLow(responseCandleLow)
        candleLows.append(candleLow)

    candleOpens = []
    for index in range(0, candleLength):
        requestCandleOpen = fetchDataSourceOpen(uuid, index)
        client.send(requestCandleOpen)
        responseCandleOpen = client.recv()
        candleOpen = parseDataSourceOpen(responseCandleOpen)
        candleOpens.append(candleOpen)

    candleCloses = []
    for index in range(0, candleLength):
        requestCandleClose = fetchDataSourceClose(uuid, index)
        client.send(requestCandleClose)
        responseCandleClose = client.recv()
        candleClose = parseDataSourceClose(responseCandleClose)
        candleCloses.append(float(candleClose))

    candleVolumes = []
    for index in range(0, candleLength):
        requestCandleVolume = fetchDataSourceVolume(uuid, index)
        client.send(requestCandleVolume)
        responseCandleVolume = client.recv()
        candleVolume = parseDataSourceVolume(responseCandleVolume)
        candleVolumes.append(int(candleVolume))

    candleTimes = []
    for index in range(0, candleLength):
        requestCandleTime = fetchDataSourceTime(uuid, index)
        client.send(requestCandleTime)
        responseCandleTime = client.recv()
        candleTime = parseDataSourceTime(responseCandleTime)
        candleTimes.append(candleTime)

    clear()
    maxHeightList(candleHeights)
    minLowList(candleLows)
    averageVolume(candleVolumes)
    averageCandleBody(candleHeights, candleLows, candleLength)
    detectImpulse(candleHeights, candleLows, candleOpens, candleCloses, candleTimes, candleVolumes, candleLength)

    requestEmptyCallback = setEmptyCallback(uuid)
    client.send(requestEmptyCallback)
    responseEmptyCallback = client.recv()
    isAwaitCallback = parseEmptyCallback(responseEmptyCallback)
    if isAwaitCallback:
        time.sleep(3)
        base(client, uuid)
    else:
        return isAwaitCallback


def getData():
    client = ctx.socket(zmq.REQ)
    client.connect('tcp://127.0.0.1:5560')

    requestDataSource = fetchDataSource()
    client.send(requestDataSource)
    responseDataSource = client.recv()
    uuid = parseDataSource(responseDataSource)

    base(client, uuid)

    requestClose = fetchDataSourceCloseSource(uuid)
    client.send(requestClose)
    responseClose = client.recv()
    isClosed = parseDataSourceCloseSource(responseClose)
    print 'isClosed ', isClosed


getData()

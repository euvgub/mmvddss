# -*- coding: utf-8 -*-

import os
import sys
import zmq
import time

from api.qlua import RPC_pb2
from api.qlua import qlua_structures_pb2
from api.qlua.datasource import CreateDataSource_pb2
from api.qlua.datasource import Size_pb2
from api.qlua.datasource import Close_pb2
from api.qlua.datasource import H_pb2
from api.qlua.datasource import L_pb2
from api.qlua.datasource import V_pb2
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


def parseDataSourceClose(message):
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

    print 'maxHeights ', maxHeights[-5:]


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

    print 'minLows ', minLows[-5:]

def averageVolume(candleVolumes):
    averageQty = sum(map(lambda qty: qty, candleVolumes)) / len(candleVolumes)
    print 'averageQty ', averageQty

def base(client, uuid):
    requestDataSourceSize = fetchDataSourceSize(uuid)
    client.send(requestDataSourceSize)
    responseDataSourceSize = client.recv()
    candleLength = parseDataSourceSize(responseDataSourceSize)
    print 'candleLength ', candleLength

    candleHeights = []
    for index in range(1, candleLength):
        requestCandleHeight = fetchDataSourceHeight(uuid, index)
        client.send(requestCandleHeight)
        responseCandleHeight = client.recv()
        candleHeight = parseDataSourceHeight(responseCandleHeight)
        candleHeights.append(candleHeight)

    candleLows = []
    for index in range(1, candleLength):
        requestCandleLow = fetchDataSourceLow(uuid, index)
        client.send(requestCandleLow)
        responseCandleLow = client.recv()
        candleLow = parseDataSourceLow(responseCandleLow)
        candleLows.append(candleLow)

    candleVolumes = []
    for index in range(1, candleLength):
        requestCandleVolume = fetchDataSourceVolume(uuid, index)
        client.send(requestCandleVolume)
        responseCandleVolume = client.recv()
        candleVolume = parseDataSourceVolume(responseCandleVolume)
        candleVolumes.append(int(candleVolume))

    clear()
    maxHeightList(candleHeights)
    minLowList(candleLows)
    averageVolume(candleVolumes)

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
    isClosed = parseDataSourceClose(responseClose)
    print 'isClosed ', isClosed


getData()

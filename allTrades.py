# -*- coding: utf-8 -*-

# 1. subscribe to 7
# 2. createDataSource

import os
import sys
import time
import signal

import zmq

from decimal import Decimal
from api.qlua import RPC_pb2
from api.qlua import qlua_structures_pb2
from api.qlua.datasource import CreateDataSource_pb2
from api.qlua.datasource import Close_pb2
from api.qlua.datasource import Size_pb2

sys.path.insert(0, './api')

ctx = zmq.Context.instance()

client = ctx.socket(zmq.REQ)
client.connect('tcp://127.0.0.1:5560')

global uuid
global lastPrice

ordersShortStack = {}
ordersLongStack = {}

orderMinuteVolume = {}
minuteVolumeLong = {}
minuteVolumeShort = {}

averageOrderValue = []

def clear(): return os.system('cls')


def current_milli_time(): return int(round(time.time() * 1000))


def fetchDataSource():
    """ Отправляет запрос на открытие источника тиковых котировок """
    message = CreateDataSource_pb2.Request()
    message.class_code = 'QJSIM'
    message.sec_code = 'SBER'
    message.interval = CreateDataSource_pb2.INTERVAL_TICK

    request = RPC_pb2.Request()
    request.type = RPC_pb2.CREATE_DATA_SOURCE
    request.args = message.SerializeToString()
    return request.SerializeToString()


def parseDataSource(message):
    """ Парси запрос на открытие источника тиковых котировок """
    response = RPC_pb2.Response()
    response.ParseFromString(message)
    messageResult = CreateDataSource_pb2.Result()
    messageResult.ParseFromString(response.result)
    print 'isOpen ', messageResult.datasource_uuid
    return messageResult.datasource_uuid


def fetchDataSourceCloseSource():
    """ Отправляет запрос на закрытие источника """
    message = Close_pb2.Request()
    message.datasource_uuid = uuid

    request = RPC_pb2.Request()
    request.type = RPC_pb2.DS_CLOSE
    request.args = message.SerializeToString()
    return request.SerializeToString()


def parseDataSourceClose(message):
    """ Парсит ответ на закрытие источника """
    response = RPC_pb2.Response()
    response.ParseFromString(message)
    messageResult = Close_pb2.Result()
    messageResult.ParseFromString(response.result)
    print 'isClosed ', messageResult.result
    return messageResult.result


def getDataSource():
    """ Запрашивает источник """
    global uuid

    client = ctx.socket(zmq.REQ)
    client.connect('tcp://127.0.0.1:5560')

    request = fetchDataSource()
    client.send(request)
    message = client.recv()
    uuid = parseDataSource(message)

    getDataSourceSize()

    subscribeOnAllTrades()


def parseAllTrades(message):
    """ Парсит тело сообщения в формат пригодный для работы с данными """
    response = qlua_structures_pb2.AllTrade()
    response.ParseFromString(message)
    return response


def subscribeOnAllTrades():
    socket = ctx.socket(zmq.SUB)
    socket.connect('tcp://127.0.0.1:5561')
    socket.subscribe('7')

    should_continue = True
    while should_continue:
        messageNumber = socket.recv()
        messageResult = socket.recv()
        # print 'message ', messageNumber
        # print 'messageResult ', messageResult
        trade = parseAllTrades(messageResult)

        volume(trade)
        if trade.flags == 1:
            setMinuteVolumeShort(trade)
            shortTrade(trade)
        else:
            setMinuteVolumeLong(trade)
            longTrade(trade)


def fetchDataSourceSize():
    message = Size_pb2.Request()
    message.datasource_uuid = uuid

    request = RPC_pb2.Request()
    request.type = RPC_pb2.DS_SIZE
    request.args = message.SerializeToString()
    return request.SerializeToString()


def parseDataSourceSize(message):
    response = RPC_pb2.Response()
    response.ParseFromString(message)
    if not response.is_error:
        messageResult = Size_pb2.Result()
        messageResult.ParseFromString(response.result)
        print "Size ", messageResult.value


def getDataSourceSize():
    request = fetchDataSourceSize()
    client.send(request)
    message = client.recv()
    parseDataSourceSize(message)


def shortTrade(trade):
    """ Собирает принты на шорт, чтобы высчитывать ускорение """
    global ordersShortStack

    averageOrderValue.append(trade.qty)
    averageQty = sum(map(lambda qty: qty, averageOrderValue)
                     ) / len(averageOrderValue)

    ms = int(round(time.time() * 1000))
    orderList = ordersShortStack.get(trade.price)
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
        print 'Sh ', trade.price, ' a:', amountQty, ' as:', averageSize, volumeByTrade(trade)

        ordersShortStack = {trade.price: orderList}
    else:
        ordersShortStack.update(
            {trade.price: [{'time': ms, 'qty': trade.qty}]})


def longTrade(trade):
    """ Собирает принты на лонг, чтобы высчитывать ускорение """
    global ordersLongStack

    averageOrderValue.append(trade.qty)
    averageQty = sum(map(lambda qty: qty, averageOrderValue)
                     ) / len(averageOrderValue)

    ms = int(round(time.time() * 1000))
    orderList = ordersLongStack.get(trade.price)
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
        print 'Lo ', trade.price, ' a:', amountQty, ' as:', averageSize, volumeByTrade(trade)

        ordersLongStack = {trade.price: orderList}
    else:
        ordersLongStack.update({trade.price: [{'time': ms, 'qty': trade.qty}]})

def setMinuteVolumeLong(trade):
    """ Считает объем в лонг по минутам """
    global minuteVolumeLong

    timeKey = str(trade.datetime.hour) + ':' + str(trade.datetime.min)
    minuteVolume = minuteVolumeLong.get(timeKey)
    if minuteVolume:
        minuteVolumeLong.update({ timeKey: minuteVolume + int(trade.qty) })
    else:
        minuteVolumeLong.update({ timeKey: trade.qty })

def setMinuteVolumeShort(trade):
    """ Считает объем в шорт по минутам """
    global minuteVolumeShort

    timeKey = str(trade.datetime.hour) + ':' + str(trade.datetime.min)
    minuteVolume = minuteVolumeShort.get(timeKey)
    if minuteVolume:
        minuteVolumeShort.update({ timeKey: minuteVolume + int(trade.qty) })
    else:
        minuteVolumeShort.update({ timeKey: trade.qty })

def volume(trade):
    """ Считает объем по минутам """
    global orderMinuteVolume

    timeKey = str(trade.datetime.hour) + ':' + str(trade.datetime.min)
    minuteVolume = orderMinuteVolume.get(timeKey)
    if minuteVolume:
        orderMinuteVolume.update({ timeKey: minuteVolume + int(trade.qty) })
    else:
        orderMinuteVolume.update({ timeKey: trade.qty })

    return orderMinuteVolume.get(timeKey)

def volumeByTrade(trade):
    """ отдает объем по минутам """
    global orderMinuteVolume

    timeKey = str(trade.datetime.hour) + ':' + str(trade.datetime.min)
    return trade.datetime.sec,  orderMinuteVolume.get(timeKey), minuteVolumeLong.get(timeKey), minuteVolumeShort.get(timeKey)

def exitScript(signum, frame):
    requestClose = fetchDataSourceCloseSource()
    client.send(requestClose)
    message = client.recv()
    parseDataSourceClose(message)
    sys.exit(1)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, exitScript)
    getDataSource()

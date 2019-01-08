# -*- coding: utf-8 -*-

import os
import sys
import time
import signal

import zmq

from api.qlua import RPC_pb2
from api.qlua import getItem_pb2
from api.qlua import qlua_structures_pb2
from api.qlua import sendTransaction_pb2


sys.path.insert(0, './api')

ctx = zmq.Context.instance()

client = ctx.socket(zmq.REQ)
client.connect('tcp://127.0.0.1:5560')

# trade_accounts - можно получить номер счета
# orders - можно получить свои ордера

def fetchItem():
    message = getItem_pb2.Request()
    message.table_name = 'orders'
    message.index = 1

    request = RPC_pb2.Request()
    request.type = RPC_pb2.GET_ITEM
    request.args = message.SerializeToString()
    return request.SerializeToString()

def parseItem(message):
    """ Парсит ответ по данным """
    response = RPC_pb2.Response()
    response.ParseFromString(message)
    # print 'res ', response
    messageResult = getItem_pb2.Result()
    messageResult.ParseFromString(response.result)
    # print 'messageResult ', messageResult.table_row
    for key in sorted(messageResult.table_row, reverse=True):
        print "%s: %s" % (key, messageResult.table_row[key])

def getItem():
    request = fetchItem()
    client.send(request)
    message = client.recv()
    parseItem(message)

# trans_params = set_value (trans_params, "ACTION", "KILL_ORDER")
# trans_params = set_value (trans_params, "ORDER_KEY", "2619254129")

# 'CLASSCODE': 'QJSIM',
# 'ACTION': 'NEW_ORDER',
# 'ACCOUNT': 'NL0011100043',
# 'OPERATION': 'S',
# 'SECCODE': 'SBER',
# 'PRICE': '210.76',
# 'QUANTITY': '1',
# 'TRANS_ID': '1',
# 'TYPE': 'L'

def fetchTransaction():
    """ Отправляет запрос на открытие источника тиковых котировок """
    order = dict({
        'CLASSCODE': 'QJSIM',
        'ACTION': 'KILL_ORDER',
        'ACCOUNT': 'NL0011100043',
        'OPERATION': 'S',
        'SECCODE': 'SBER',
        'PRICE': '210.76',
        'QUANTITY': '1',
        'TRANS_ID': '1',
        'TYPE': 'L',
        'ORDER_KEY': '4132996527'
    })
    message = sendTransaction_pb2.Request(transaction=order)

    request = RPC_pb2.Request()
    request.type = RPC_pb2.SEND_TRANSACTION
    request.args = message.SerializeToString()
    return request.SerializeToString()

def parseTransaction(message):
    """ Парсит ответ по транзакции """
    response = RPC_pb2.Response()
    response.ParseFromString(message)
    messageResult = sendTransaction_pb2.Result()
    messageResult.ParseFromString(response.result)
    print 'messageResult ', messageResult.result

def sendTransaction():
    """ Отправляет и парсит ответ по заявке """
    request = fetchTransaction()
    client.send(request)
    message = client.recv()
    parseTransaction(message)

# sendTransaction()
getItem()
# 1. subscribe to 7
# 2. createDataSource

import sys
import time

import zmq

from api.qlua import RPC_pb2
from api.qlua import qlua_structures_pb2
from api.qlua.datasource import CreateDataSource_pb2
from api.qlua.datasource import Size_pb2

sys.path.insert(0, './api')

ctx = zmq.Context.instance()


def fetchDataSource():
    message = CreateDataSource_pb2.Request()
    message.class_code = 'QJSIM'
    message.sec_code = 'SBER'
    message.interval = CreateDataSource_pb2.INTERVAL_TICK

    request = RPC_pb2.Request()
    request.type = RPC_pb2.CREATE_DATA_SOURCE
    request.args = message.SerializeToString()
    print "Request ", request
    return request.SerializeToString()


def parseDataSource(message):
    response = RPC_pb2.Response()
    response.ParseFromString(message)
    messageResult = CreateDataSource_pb2.Result()
    messageResult.ParseFromString(response.result)
    print "Response ", messageResult


def getDataSource():
    request = fetchDataSource()

    client = ctx.socket(zmq.REQ)
    client.connect('tcp://127.0.0.1:5560')
    client.send(request)

    for request in range(1):
        message = client.recv()
        parseDataSource(message)


def parseAllTrades(message):
    response = qlua_structures_pb2.AllTrade()
    response.ParseFromString(message)
    print "Response result", response


def subscribeOnAllTrades():
    socket = ctx.socket(zmq.SUB)
    socket.connect('tcp://127.0.0.1:5561')
    socket.subscribe('7')

    should_continue = True
    while should_continue:
        messageNumber = socket.recv()
        messageResult = socket.recv()
        # print "Received message number", messageNumber
        # print "Received message result", messageResult
        parseAllTrades(messageResult)


def fetchDataSourceSize():
    message = Size_pb2.Request()
    message.datasource_uuid = 'dc35c7d7-ffff-4c64-cc4c-d7066017ad0e'

    request = RPC_pb2.Request()
    request.type = RPC_pb2.DS_SIZE
    request.args = message.SerializeToString()
    print "Request ", request
    return request.SerializeToString()


def parseDataSourceSize(message):
    response = RPC_pb2.Response()
    response.ParseFromString(message)
    messageResult = Size_pb2.Result()
    messageResult.ParseFromString(response.result)
    print "Response ", messageResult


def getDataSourceSize():
    request = fetchDataSourceSize()

    client = ctx.socket(zmq.REQ)
    client.connect('tcp://127.0.0.1:5560')
    client.send(request)

    for request in range(1):
        message = client.recv()
        parseDataSourceSize(message)


# getDataSource()
getDataSourceSize()

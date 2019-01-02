from api.qlua import isConnected_pb2
from api.qlua import RPC_pb2
from api.qlua import message_pb2
from api.qlua import Subscribe_Level_II_Quotes_pb2

import sys
import time

import zmq

ctx = zmq.Context.instance()

sys.path.insert(0, './api')


def buildRPCSubscribeLevelII():
    message = Subscribe_Level_II_Quotes_pb2.Request()
    message.class_code = 'QJSIM'
    message.sec_code = 'SBER'

    request = RPC_pb2.Request()
    request.type = RPC_pb2.SUBSCRIBE_LEVEL_II_QUOTES
    request.args = message.SerializeToString()
    return request.SerializeToString()


def parseRPCSubscribeLevelII(message):
    response = RPC_pb2.Response()
    response.ParseFromString(message)
    messageResult = Subscribe_Level_II_Quotes_pb2.Result()
    messageResult.ParseFromString(response.result)
    print "Response ", messageResult


def subscribeLevelTII():
    request = buildRPCSubscribeLevelII()

    client = ctx.socket(zmq.REQ)
    client.connect('tcp://127.0.0.1:5560')
    client.send(request)

    while True:
        message = client.recv()
        parseRPCSubscribeLevelII(message)
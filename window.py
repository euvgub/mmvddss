import sys
import time

import zmq

from api.qlua import AllocTable_pb2
from api.qlua import CreateWindow_pb2
from api.qlua import RPC_pb2

ctx = zmq.Context.instance()

sys.path.insert(0, './api')

# 1. allocTable
# 2. createWindow


def buildRPCAllocTable():
    request = RPC_pb2.Request()
    request.type = RPC_pb2.ALLOC_TABLE
    return request.SerializeToString()


def parseRPCAllocTable(message):
    response = RPC_pb2.Response()
    response.ParseFromString(message)
    messageResult = AllocTable_pb2.Result()
    messageResult.ParseFromString(response.result)
    print "Response allow table", messageResult
    return messageResult.t_id


def buildRPCCreateWindow(id):
    message = CreateWindow_pb2.Request()
    message.t_id = id

    request = RPC_pb2.Request()
    request.type = RPC_pb2.CREATE_WINDOW
    request.args = message.SerializeToString()
    return request.SerializeToString()


def parseRPCCreateWindow(message):
    response = RPC_pb2.Response()
    response.ParseFromString(message)
    messageResult = CreateWindow_pb2.Result()
    messageResult.ParseFromString(response.result)
    print "Response on create window", messageResult
    return messageResult


def createWindow():
    request = buildRPCAllocTable()

    client = ctx.socket(zmq.REQ)
    client.connect('tcp://127.0.0.1:5560')
    client.send(request)

    for request in range(1):
        message = client.recv()
        createWindowRequest = buildRPCCreateWindow(parseRPCAllocTable(message))

    client.send(createWindowRequest)
    for request in range(1):
        message = client.recv()
        parseRPCCreateWindow(message)


createWindow()

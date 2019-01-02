# -*- coding: utf-8 -*-
#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

from api.qlua import isConnected_pb2
from api.qlua import RPC_pb2
from api.qlua import message_pb2
from api.qlua import getQuoteLevel2_pb2

import sys
import time

import zmq

ctx = zmq.Context.instance()

sys.path.insert(0, './api')


def buildRPCMessage():
    message = message_pb2.Request()
    message.message = 'Hello world'
    message.icon_type = message_pb2.INFO

    request = RPC_pb2.Request()
    request.type = RPC_pb2.MESSAGE
    request.args = message.SerializeToString()
    return request.SerializeToString()


def parseMessageResponse(message):
    print "Message ", message
    response = RPC_pb2.Response()
    response.ParseFromString(message)
    messageResult = message_pb2.Result()
    messageResult.ParseFromString(response.result)
    print "Response ", messageResult


def buildRPCIsConnected():
    request = RPC_pb2.Request()
    request.type = RPC_pb2.IS_CONNECTED
    return request.SerializeToString()


def parseIsConnectedResponse(message):
    print "Message ", message
    response = RPC_pb2.Response()
    response.ParseFromString(message)
    messageResult = message_pb2.Result()
    messageResult.ParseFromString(response.result)
    print "Response ", messageResult


def run():
    client = ctx.socket(zmq.REQ)
    # client.plain_username = 'U0132810'
    # client.plain_password = '04334'
    client.connect('tcp://127.0.0.1:5560')

    rpc = buildRPCIsConnected()
    print "protoMsg ", rpc

    for request in range(1):
        print "Sending request ", request
        client.send(rpc)
        messageFrame = client.recv()
        print "bufferMessage ", messageFrame
        parseIsConnectedResponse(messageFrame)
        time.sleep(1)


def subscribeQuoteLevelII():
    socket = ctx.socket(zmq.SUB)
    socket.connect('tcp://127.0.0.1:5561')
    socket.subscribe('24')

    should_continue = True
    while should_continue:
        messageNumber = socket.recv()
        messageResult = socket.recv()
        print "Received message number", messageNumber
        print "Received message result", messageResult
        getQuoteLevelII()


def fetchQuoteLevelII():
    message = getQuoteLevel2_pb2.Request()
    message.class_code = 'QJSIM'
    message.sec_code = 'SBER'

    request = RPC_pb2.Request()
    request.type = RPC_pb2.GET_QUOTE_LEVEL2
    request.args = message.SerializeToString()
    return request.SerializeToString()


def parseQuoteLevelII(message):
    response = RPC_pb2.Response()
    response.ParseFromString(message)
    messageResult = getQuoteLevel2_pb2.Result()
    messageResult.ParseFromString(response.result)
    print "Response ", messageResult


def getQuoteLevelII():
    request = fetchQuoteLevelII()

    client = ctx.socket(zmq.REQ)
    client.connect('tcp://127.0.0.1:5560')
    client.send(request)

    for request in range(1):
        message = client.recv()
        parseQuoteLevelII(message)


subscribeQuoteLevelII()

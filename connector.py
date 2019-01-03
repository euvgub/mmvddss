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

import os
import sys
import time
from decimal import Decimal

import zmq

clear = lambda: os.system('cls')

# client.plain_username = 'U0132810'
# client.plain_password = '04334'

sys.path.insert(0, './api')

ctx = zmq.Context.instance()
client = ctx.socket(zmq.REQ)
client.connect('tcp://127.0.0.1:5560')

bidsStack = {}
offersStack = {}


def subscribeQuoteLevelII():
    socket = ctx.socket(zmq.SUB)
    socket.connect('tcp://127.0.0.1:5561')
    socket.subscribe('24')

    should_continue = True
    while should_continue:
        messageNumber = socket.recv()
        messageResult = socket.recv()
        # print "Received message number", messageNumber
        # print "Received message result", messageResult
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
    # print 'Offers', messageResult.offers
    # print 'Bids', messageResult.bids
    clear()
    updateOfferStack(messageResult.offers)
    updateBidStack(messageResult.bids)


def getQuoteLevelII():
    request = fetchQuoteLevelII()
    client.send(request)
    message = client.recv()
    parseQuoteLevelII(message)


def updateOfferStack(offers):
    """ Содержит заявки на продажи с их измененным состоянием относительно пред. изменения """
    global offersStack
    offersPrice = []
    for offerIndex in range(len(offers)):
        offersPrice.append(offers[offerIndex].price)

    offersStackCopy = {}
    for offerPriceIndex in range(len(offersPrice)):
        price = offersPrice[offerPriceIndex]
        if price in offersStack:
            offersStackCopy.update({ price: offersStack[price] })

    offersStack = dict(offersStackCopy)
    for offerIndex in range(len(offers)):
        offer = offers[offerIndex]
        offerStack = offersStack.get(offer.price)
        change = 0

        if offerStack:
            change = 100 * (int(offer.quantity) -
                            offerStack.get('value')) / offerStack.get('value')
            inserter = {}
            inserterChild = {
                'value': int(offer.quantity),
                'change': change
            }
            inserter[offer.price] = inserterChild
            offersStack.update(inserter)
        else:
            offersStack.update(
                {offer.price: {'value': int(offer.quantity), 'change': 0}})
    print 'change offer ---'
    for key in sorted(offersStack, reverse=True):
        print "%s: %s" % (key, offersStack[key])


def updateBidStack(bids):
    """ Содержит заявки на покупки с их измененным состоянием относительно пред. изменения """
    global bidsStack
    bidsPrice = []
    for bidIndex in range(len(bids)):
        bidsPrice.append(bids[bidIndex].price)

    bidsStackCopy = {}
    for bidPriceIndex in range(len(bidsPrice)):
        price = bidsPrice[bidPriceIndex]
        if price in bidsStack:
            bidsStackCopy.update({ price: bidsStack[price] })

    bidsStack = dict(bidsStackCopy)
    for bidIndex in range(len(bids)):
        bid = bids[bidIndex]
        bidStack = bidsStack.get(bid.price)
        change = 0

        if bidStack:
            change = 100 * (int(bid.quantity) -
                            bidStack.get('value')) / bidStack.get('value')
            inserter = {}
            inserterChild = {
                'value': int(bid.quantity),
                'change': change
            }
            inserter[bid.price] = inserterChild
            bidsStack.update(inserter)
        else:
            bidsStack.update(
                {bid.price: {'value': int(bid.quantity), 'change': 0}})
    print 'change bid ---'
    for key in sorted(bidsStack, reverse=True):
        print "%s: %s" % (key, bidsStack[key])


subscribeQuoteLevelII()

# -*- coding: utf-8 -*-

import sys

from api.qlua import RPC_pb2
from api.qlua import qlua_structures_pb2
from api.qlua import getQuoteLevel2_pb2
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


class Request:
    def fetchDataSourceGraph(self):
        """ Запрашивает создание источника данных для свечек """
        message = CreateDataSource_pb2.Request()
        message.class_code = 'QJSIM'
        message.sec_code = 'SBER'
        message.interval = CreateDataSource_pb2.INTERVAL_M1

        request = RPC_pb2.Request()
        request.type = RPC_pb2.CREATE_DATA_SOURCE
        request.args = message.SerializeToString()
        print "Request ", request
        return request.SerializeToString()

    def parseDataSourceGraph(self, message):
        """ Парсит создание источника данных для свечек, вытаскивает uuid в терминале для этого источника """
        response = RPC_pb2.Response()
        response.ParseFromString(message)
        messageResult = CreateDataSource_pb2.Result()
        messageResult.ParseFromString(response.result)
        print "Response ", messageResult
        return messageResult.datasource_uuid

    def fetchDataSourceCloseSourceGraph(self, uuid):
        """ Отправляет запрос на закрытие источника """
        message = Close_pb2.Request()
        message.datasource_uuid = uuid

        request = RPC_pb2.Request()
        request.type = RPC_pb2.DS_CLOSE
        request.args = message.SerializeToString()
        return request.SerializeToString()

    def parseDataSourceCloseSourceGraph(self, message):
        """ Парсит ответ на закрытие источника """
        response = RPC_pb2.Response()
        response.ParseFromString(message)
        messageResult = Close_pb2.Result()
        messageResult.ParseFromString(response.result)
        return messageResult.result

    def fetchDataSourceSizeGraph(self, uuid):
        """ Запрашивает по uuid источника количество отданных  с сервера свечей """
        message = Size_pb2.Request()
        message.datasource_uuid = uuid

        request = RPC_pb2.Request()
        request.type = RPC_pb2.DS_SIZE
        request.args = message.SerializeToString()
        return request.SerializeToString()

    def parseDataSourceSizeGraph(self, message):
        """ Парсит количество отданных свечей """
        response = RPC_pb2.Response()
        response.ParseFromString(message)
        messageResult = Size_pb2.Result()
        messageResult.ParseFromString(response.result)
        return messageResult.value

    def fetchDataSourceHeightGraph(self, uuid, index):
        """ Запрашивает высоту свечи в потоке и от индекса свечи """
        message = H_pb2.Request()
        message.datasource_uuid = uuid
        message.candle_index = index

        request = RPC_pb2.Request()
        request.type = RPC_pb2.DS_H
        request.args = message.SerializeToString()
        return request.SerializeToString()

    def parseDataSourceHeightGraph(self, message):
        """ Парсит высоту свечи """
        response = RPC_pb2.Response()
        response.ParseFromString(message)
        messageResult = H_pb2.Result()
        messageResult.ParseFromString(response.result)
        return messageResult.value

    def fetchDataSourceLowGraph(self, uuid, index):
        """ Запрашивает высоту свечи в потоке и от индекса свечи """
        message = L_pb2.Request()
        message.datasource_uuid = uuid
        message.candle_index = index

        request = RPC_pb2.Request()
        request.type = RPC_pb2.DS_L
        request.args = message.SerializeToString()
        return request.SerializeToString()

    def parseDataSourceLowGraph(self, message):
        """ Парсит высоту свечи """
        response = RPC_pb2.Response()
        response.ParseFromString(message)
        messageResult = L_pb2.Result()
        messageResult.ParseFromString(response.result)
        return messageResult.value

    def fetchDataSourceOpenGraph(self, uuid, index):
        """ Запрашивает открытие свечи в потоке и от индекса свечи """
        message = O_pb2.Request()
        message.datasource_uuid = uuid
        message.candle_index = index

        request = RPC_pb2.Request()
        request.type = RPC_pb2.DS_O
        request.args = message.SerializeToString()
        return request.SerializeToString()

    def parseDataSourceOpenGraph(self, message):
        """ Запрашивает открытие свечи в потоке и от индекса свечи """
        response = RPC_pb2.Response()
        response.ParseFromString(message)
        messageResult = O_pb2.Result()
        messageResult.ParseFromString(response.result)
        return messageResult.value

    def fetchDataSourceCloseGraph(self, uuid, index):
        """ Запрашивает закрытие свечи в потоке и от индекса свечи """
        message = C_pb2.Request()
        message.datasource_uuid = uuid
        message.candle_index = index

        request = RPC_pb2.Request()
        request.type = RPC_pb2.DS_C
        request.args = message.SerializeToString()
        return request.SerializeToString()

    def parseDataSourceCloseGraph(self, message):
        """ Запрашивает закрытие свечи в потоке и от индекса свечи """
        response = RPC_pb2.Response()
        response.ParseFromString(message)
        messageResult = C_pb2.Result()
        messageResult.ParseFromString(response.result)
        return messageResult.value

    def fetchDataSourceTimeGraph(self, uuid, index):
        """ Запрашивает время свечи в потоке и от индекса свечи """
        message = T_pb2.Request()
        message.datasource_uuid = uuid
        message.candle_index = index

        request = RPC_pb2.Request()
        request.type = RPC_pb2.DS_T
        request.args = message.SerializeToString()
        return request.SerializeToString()

    def parseDataSourceTimeGraph(self, message):
        """ Запрашивает время свечи в потоке и от индекса свечи """
        response = RPC_pb2.Response()
        response.ParseFromString(message)
        messageResult = T_pb2.Result()
        messageResult.ParseFromString(response.result)
        return messageResult

    def fetchDataSourceVolumeGraph(self, uuid, index):
        """ Запрашивает объем свечи в потоке и от индекса свечи """
        message = V_pb2.Request()
        message.datasource_uuid = uuid
        message.candle_index = index

        request = RPC_pb2.Request()
        request.type = RPC_pb2.DS_V
        request.args = message.SerializeToString()
        return request.SerializeToString()

    def parseDataSourceVolumeGraph(self, message):
        """ Парсит объем свечи """
        response = RPC_pb2.Response()
        response.ParseFromString(message)
        messageResult = V_pb2.Result()
        messageResult.ParseFromString(response.result)
        return messageResult.value

    def setEmptyCallbackGraph(self, uuid):
        """ Ставит пустой колбек """
        message = SetEmptyCallback_pb2.Request()
        message.datasource_uuid = uuid

        request = RPC_pb2.Request()
        request.type = RPC_pb2.DS_SET_EMPTY_CALLBACK
        request.args = message.SerializeToString()
        return request.SerializeToString()

    def parseEmptyCallbackGraph(self, message):
        """ Парсит ответ на пустой колбек """
        response = RPC_pb2.Response()
        response.ParseFromString(message)
        messageResult = SetEmptyCallback_pb2.Result()
        messageResult.ParseFromString(response.result)
        return messageResult.result

    def fetchDataSourceTrade(self):
        """ Отправляет запрос на открытие источника тиковых котировок """
        message = CreateDataSource_pb2.Request()
        message.class_code = 'QJSIM'
        message.sec_code = 'SBER'
        message.interval = CreateDataSource_pb2.INTERVAL_TICK

        request = RPC_pb2.Request()
        request.type = RPC_pb2.CREATE_DATA_SOURCE
        request.args = message.SerializeToString()
        return request.SerializeToString()

    def parseDataSourceTrade(self, message):
        """ Парси запрос на открытие источника тиковых котировок """
        response = RPC_pb2.Response()
        response.ParseFromString(message)
        messageResult = CreateDataSource_pb2.Result()
        messageResult.ParseFromString(response.result)
        print 'isOpen ', messageResult.datasource_uuid
        return messageResult.datasource_uuid

    def fetchDataSourceCloseSourceTrade(self, uuid):
        """ Отправляет запрос на закрытие источника """
        message = Close_pb2.Request()
        message.datasource_uuid = uuid

        request = RPC_pb2.Request()
        request.type = RPC_pb2.DS_CLOSE
        request.args = message.SerializeToString()
        return request.SerializeToString()

    def parseDataSourceCloseTrade(self, message):
        """ Парсит ответ на закрытие источника """
        response = RPC_pb2.Response()
        response.ParseFromString(message)
        messageResult = Close_pb2.Result()
        messageResult.ParseFromString(response.result)
        print 'isClosed ', messageResult.result
        return messageResult.result

    def setEmptyCallbackTrade(self, uuid):
        """ Ставит пустой колбек """
        message = SetEmptyCallback_pb2.Request()
        message.datasource_uuid = uuid

        request = RPC_pb2.Request()
        request.type = RPC_pb2.DS_SET_EMPTY_CALLBACK
        request.args = message.SerializeToString()
        return request.SerializeToString()

    def parseEmptyCallbackTrade(self, message):
        """ Парсит ответ на пустой колбек """
        response = RPC_pb2.Response()
        response.ParseFromString(message)
        messageResult = SetEmptyCallback_pb2.Result()
        messageResult.ParseFromString(response.result)
        return messageResult.result

    def parseAllTrades(self, message):
        """ Парсит тело сообщения в формат пригодный для работы с данными """
        response = qlua_structures_pb2.AllTrade()
        response.ParseFromString(message)
        return response

    def fetchDataSourceSizeTrade(self, uuid):
        message = Size_pb2.Request()
        message.datasource_uuid = uuid

        request = RPC_pb2.Request()
        request.type = RPC_pb2.DS_SIZE
        request.args = message.SerializeToString()
        return request.SerializeToString()

    def parseDataSourceSizeTrade(self, message):
        response = RPC_pb2.Response()
        response.ParseFromString(message)
        if not response.is_error:
            messageResult = Size_pb2.Result()
            messageResult.ParseFromString(response.result)
            print "Size ", messageResult.value

    def fetchQuoteLevelIIConnector(self):
        message = getQuoteLevel2_pb2.Request()
        message.class_code = 'QJSIM'
        message.sec_code = 'SBER'

        request = RPC_pb2.Request()
        request.type = RPC_pb2.GET_QUOTE_LEVEL2
        request.args = message.SerializeToString()
        return request.SerializeToString()

    def parseQuoteLevelIIConnector(self, message):
        response = RPC_pb2.Response()
        response.ParseFromString(message)
        messageResult = getQuoteLevel2_pb2.Result()
        messageResult.ParseFromString(response.result)
        return messageResult

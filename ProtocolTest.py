import time
from re import *

class ProtocolT:


    def __init__(self):
        self.time = ''
        self.operation = ''
        self.liczb1 = ''
        self.liczb2 = ''
        self.liczb3 = ''
        self.wynik = ''
        self.status = ''
        self.identy = ''
        self.allMessage = ''


    def messageToServer(self):
        self.allMessage = "CzasKm>>" + self.time + "^OperaC>>" + self.operation + "^Liczb1>>" + self.liczb1 + "^Liczb2>>" + self.liczb2 + "^Liczb3>>" + self.liczb3 +"^StatuS>>" + self.status + "^IdentY>>" + self.identy + "^"


    def conectOrDiswithServer(self):
        self.allMessage = "CzasKm>>" + self.time + "^OperaC>>" + self.operation +"^StatuS>>" + self.status + "^IdentY>>" + self.identy + "^"

    def sendResultToClient(self):
        self.allMessage = "CzasKm>>" + self.time + "^OperaC>>" + self.operation + "^WynOpe>>"+ self.wynik + "^StatuS>>" + self.status + "^IdentY>>" + self.identy + "^"

    def sendMessageToServer(self):
        self.allMessage = "CzasKm>>" + self.time + "^OperaC>>" + self.operation + "^StatuS>>" + self.status+ "^IdentY>>" + self.identy + "^"




    def encodeMessageToServer(self, num1, num2, num3, op, id, stat, tim):

        self.liczb1 = str(num1)
        self.liczb2 = str(num2)
        self.liczb3 = str(num3)
        self.operation = op
        self.identy = id
        self.status = str(stat)
        self.time = tim
        self.messageToServer()
        message=self.allMessage.encode('utf-8')
        return message

    def encodeMessageToClientWithResult(self, op,id,stat,tim,wyn):

        self.operation = op
        self.identy = id
        self.status = stat
        self.time = tim
        self.wynik = wyn
        self.sendResultToClient()
        message = self.allMessage.encode('utf-8')
        return message


    def encodeMessageToServerToWantIdenty(self, op,stat,tim, id):

        self.operation = op
        self.status = stat
        self.time = tim
        self.identy=id
        self.sendMessageToServer()
        message = self.allMessage.encode('utf-8')
        return message

    def decodeMesgageFromClientIDENTY(self, message):
        self.allMessage = message
        decMessage = self.allMessage.decode('utf-8')
        data = findall('>>(.*?)\^', decMessage)
        self.time = data[0]
        self.operation = data[1]
        self.status = data[2]
        self.identy = data[3]
        self.conectOrDiswithServer()

    def enconeMessageToClientFirstOrLast(self, op,id, stat, tim):

        self.operation = op
        self.identy = id
        self.status = stat
        self.time = tim
        self.conectOrDiswithServer()
        message = self.allMessage.encode('utf-8')
        return message

    def decodeMessageFromServerFirts(self, message):
        self.allMessage = message
        decMessage = self.allMessage.decode('utf-8')
        data = findall('>>(.*?)\^', decMessage)
        self.time = data[0]
        self.operation = data[1]
        self.status = data[2]
        self.identy = data[3]
        self.conectOrDiswithServer()


    def decodeMessageFromClient(self, message):
        self.allMessage = message
        decMessage = self.allMessage.decode('utf-8')
        data = findall('>>(.*?)\^', decMessage)
        self.time = data[0]
        self.operation = data[1]
        self.liczb1 = data[2]
        self.liczb2 = data[3]
        self.liczb3 = data[4]
        self.status = data[5]
        self.identy = data[6]
        self.messageToServer()

    def decodeMessageFromServertSecond(self, message):
        self.allMessage = message
        decMessage = self.allMessage.decode('utf-8')
        data = findall('>>(.*?)\^', decMessage)
        self.time = data[0]
        self.operation = data[1]
        self.wynik = data[2]
        self.status = data[3]
        self.identy = data[4]
        self.sendResultToClient()

    def decodeProtocol(self, message):
        self.allMessage = message
        decMessage = self.allMessage.decode('utf-8')
        data = findall('>>(.*?)\^', decMessage)
        self.time = data[0]
        self.operation = data[1]
        self.liczb1 = data[2]
        self.liczb2 = data[3]
        self.liczb3 = data[4]
        self.wynik = data[5]
        self.status = data[6]
        self.identy = data[7]
        self.cerateAllProtocol()








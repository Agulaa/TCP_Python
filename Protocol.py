import time
from re import *

class Protocol:


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
        """Sklejenie pakietu do wysłania, ktory wysyła klient do sewera z liczbami i operacją """
        self.allMessage = "CzasMs>>" + self.time + "^OperaC>>" + self.operation + "^Liczb1>>" + self.liczb1 + "^Liczb2>>" + self.liczb2 + "^Liczb3>>" + self.liczb3 +"^StatuS>>" + self.status + "^IdentY>>" + self.identy + "^"


    def conectOrDiswithServer(self):
        """Sklejenie pakietu używanego podczas nawiązywania połączenia lub zakończenia"""
        self.allMessage = "CzasMs>>" + self.time + "^OperaC>>" + self.operation +"^StatuS>>" + self.status + "^IdentY>>" + self.identy + "^"

    def sendResultToClient(self):
        """Sklejanie pakietu używanego do wysyłania przez serwer wyniku dla klienta """
        self.allMessage = "CzasMs>>" + self.time + "^OperaC>>" + self.operation + "^WynOpe>>"+ self.wynik + "^StatuS>>" + self.status + "^IdentY>>" + self.identy + "^"





    def encodeMessageToServer(self, num1, num2, num3, op, id, stat, tim):
        """Zakodowanie wiadomości do wysłania przez klienta z liczbami i operacją"""

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
        """Zakodowanie wiadomości do wysłania przez serwer z wynikiem dla klienta """

        self.operation = op
        self.identy = id
        self.status = stat
        self.time = tim
        self.wynik = wyn
        self.sendResultToClient()
        message = self.allMessage.encode('utf-8')
        return message


    def encodeMessageToServerToWantIdentyOrDsiconnect(self, op,stat,tim, id):
        """Zakodowanie wiadomości klienta, ktory laczy się z serwerem"""

        self.operation = op
        self.status = stat
        self.time = tim
        self.identy=id
        self.conectOrDiswithServer()
        message = self.allMessage.encode('utf-8')
        return message

    def decodeMesgageFromClientIDENTY(self, message):
        """Odkodowanie wiadmości od klienta , ktory chce uzyskać identyfikator sesji"""
        self.allMessage = message
        decMessage = self.allMessage.decode('utf-8')
        self.time = findall('CzasMs>>(.*?)\^', decMessage)[0]
        self.operation = findall('OperaC>>(.*?)\^', decMessage)[0]
        self.status = findall('StatuS>>(.*?)\^', decMessage)[0]
        self.identy = findall('IdentY>>(.*?)\^', decMessage)[0]
        self.conectOrDiswithServer()



    def decodeMessageFromClient(self, message):
        """Odkodowanie wiadomości od klienta, który wysyła operację oraz liczby"""
        self.allMessage = message
        decMessage = self.allMessage.decode('utf-8')
        self.time = findall('CzasMs>>(.*?)\^', decMessage)[0]
        self.operation = findall('OperaC>>(.*?)\^', decMessage)[0]
        if  self.operation !='DISCONNECT':
            self.liczb1 = findall('Liczb1>>(.*?)\^', decMessage)[0]
            self.liczb2 = findall('Liczb2>>(.*?)\^', decMessage)[0]
            self.liczb3 = findall('Liczb3>>(.*?)\^', decMessage)[0]
            self.status = findall('StatuS>>(.*?)\^', decMessage)[0]
            self.identy = findall('IdentY>>(.*?)\^', decMessage)[0]
            self.messageToServer()
        else:
            self.status = findall('StatuS>>(.*?)\^', decMessage)[0]
            self.identy = findall('IdentY>>(.*?)\^', decMessage)[0]
            self.conectOrDiswithServer()


    def decodeMessageFromServertSecond(self, message):
        """Odkodwanie wiadomości od serwera z wynikiem operacji"""
        self.allMessage = message
        decMessage = self.allMessage.decode('utf-8')
        self.time = findall('CzasMs>>(.*?)\^', decMessage)[0]
        self.operation = findall('OperaC>>(.*?)\^', decMessage)[0]
        self.wynik = findall('WynOpe>>(.*?)\^', decMessage)[0]
        self.status = findall('StatuS>>(.*?)\^', decMessage)[0]
        self.identy = findall('IdentY>>(.*?)\^', decMessage)[0]
        self.sendResultToClient()









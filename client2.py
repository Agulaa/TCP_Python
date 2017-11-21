from socket import *
from re import *
import time
from allPacket import  *
import threading
class TCPClient:

         def __init__(self):
            self.host = '127.0.0.1'
            self.port = 8080
            self.buffer = 1024
            self.identSe = '0'
            self.socket = socket(AF_INET, SOCK_STREAM)

         def GetOperationAndNumbers(self):
             op = input('Podaj operacje ["op1"(-) ,"op2" (:),"op3" (*),"op4" (+)')
             one = input('Podaj 1 argumen')
             two = input('Podaj 2 argument')
             three = input('Podaj 3 argument')
             result = [op,one,two,three]
             return result

         def connAndRecvFromServer(self):

             self.socket.connect((self.host, self.port))
             print('Connect')
             #uzgodnienie identyfikaytora sesji
             packet = allPacket()
             message = self.socket.recv(self.buffer)

             packet.decodePacket(message)
             print(packet.allMessage)
             if packet.operation == 'con':
                 self.identSe = packet.identy



         def sendPacketToServer(self):

             packet = allPacket()
             result = self.GetOperationAndNumbers()
             localtime = time.asctime(time.localtime(time.time()))
             mesage= packet.encodePacket(result[1], result[2], result[3], result[0],self.identSe,' ', localtime)
             self.socket.send(mesage)
             print(packet.allMessage)

         def answerFromServer(self):
             while True:
                 packet = allPacket()
                 message = self.socket.recv(self.buffer)
                 packet.decodePacket(message)
                 packet.printAllPacket()
                 if packet.operation == 'ok':
                     print('Operacja na trzech argumentach zostala dobrze wykonana')
                     self.socket.close()

                 elif packet.operation == 'error':
                     print('Operacja na trzech argumentach nie zostala poprawnie wykonana')
                     self.socket.close()





         def run(self):
              self.connAndRecvFromServer()
              self.sendPacketToServer()
              self.answerFromServer()



def Main():
    client = TCPClient()
    client.run()



if __name__=='__main__':
    Main()




from socket import *
from re import *
import time
import threading
class TCPClient:

         def __init__(self):
            self.host = '127.0.0.1'
            self.port = 8080
            self.time = ''
            self.operation = ''
            self.liczb1 = ''
            self.liczb2 = ''
            self.liczb3 = ''
            self.l1=0
            self.l2=0
            self.l3=0
            self.status = ''
            self.clientID =0
            self.threads = []
            self.allPacket = ''
            self.client=''



         def connection(self):
             self.client = socket(AF_INET, SOCK_STREAM)
             print('Klient')
             try:
                 self.client.connect((self.host, self.port))
             except socket.error as e:
                 print('Error')


         def createAllPacket(self):
                 self.allPacket = "CzasKm>>" + self.time + "^" + "OperaC>>" + self.operation + "^" +"Liczb1>>" + self.liczb1 + "^" + "Liczb2>>" + self.liczb2 +"^" + "Liczb3>>" + self.liczb3 +"^" + "StatuS>>" + self.status + "^" +"IdentY>>" + str(self.clientID) + "^"

         def printRecvPaceket(self):
             print('---------------------------')
             print('Klient otrzymal:')
             recvPakcet = findall('(.*?)\^', self.allPacket)
             for i in recvPakcet:
                 print(i)
             print('---------------------------')

         def printSendPacket(self):
             print('+++++++++++++++++++++++++++')
             print('Klient wysyla:')
             recvPakcet = findall('(.*?)\^', self.allPacket)
             for i in recvPakcet:
                 print(i)
             print('+++++++++++++++++++++++++++')

         def recvPacket(self):
             data = self.client.recv(1024)
             data = data.decode('ascii')
             #recvPakcet1 = findall('>>[a-zA-Z0-9 :]*\^\n', data)
             recvPakcet = findall('>>(.*?)\^', data)  # (.*?) oznacza niezachłanne dopasowanie znaków za wyjątkiem znaku 'n'.
             print('recvPacket')
             print(recvPakcet)
             self.time = recvPakcet[0]
             self.operation = recvPakcet[1]
             self.liczb1 = recvPakcet[2]
             self.liczb2 = recvPakcet[3]
             self.liczb3 = recvPakcet[4]
             self.status = recvPakcet[5]
             self.clientID = recvPakcet[6]
             self.createAllPacket()
             self.printRecvPaceket()


         def sendPacket(self):
             self.time = time.ctime(time.time())
             self.GetOperationAndNumbers()
             self.createAllPacket()
             self.client.send(self.allPacket.encode('ascii'))
             self.printSendPacket()

         # op1- odejmowanie, op2- dzielenie, op3- mnozenie, op4- dodawanie
         def GetOperationAndNumbers(self):

               op= input('Podaj operacje ["op1"(-) ,"op2" (:),"op3" (*),"op4" (+)')
               self.operation = op
               one = input('Podaj 1 argumen')
               two = input('Podaj 2 argument')
               tree = input('Podaj 3 argument')
               self.liczb1 =one
               self.liczb2 = two
               self.liczb3 = tree

         def run(self):
                 self.connection()
                 self.sendPacket()
                 self.recvPacket()
                 #self.sendPacket()
                 #self.recvPacket()







def Main():
    client = TCPClient()
    client.run()



if __name__=='__main__':
    Main()




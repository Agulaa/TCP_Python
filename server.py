from socket import *
from threading import Lock, Thread
import time
from re import *

class TCPServer:

        def __init__(self):
            self.host = '127.0.0.1'
            self.port = 8080
            self.time = ''
            self.operation = ''
            self.liczb1 = ''
            self.liczb2 = ''
            self.liczb3 = ''
            self.l1 = 0
            self.l2 = 0
            self.l3 = 0
            self.status = ''
            self.threads = []
            self.allPacket = ''
            self.server = ''
            self.clientID='0'
            self.id=0
            self.client=''


        def connection(self):
            self.server = socket(AF_INET, SOCK_STREAM)
            print('SERVER WAIT FOR CONNECTION')
            print('--------------------------')
            try:
               self.server.bind((self.host, self.port))
            except error as e:
                print(str(e))
            self.server.listen(5)
            self.client, addr = self.server.accept()
            self.id=self.id+1
            print('Server polaczony  z ' +str(self.clientID ))


        def createAllPacket(self):
                 self.allPacket = "CzasKm>>" + self.time + "^" + "OperaC>>" + self.operation + "^" +"Liczb1>>" + self.liczb1 + "^" + "Liczb2>>" + self.liczb2 +"^" + "Liczb3>>" + self.liczb3 +"^" + "StatuS>>" + self.status + "^" +"IdentY>>" + str(self.clientID) + "^"
        def printRecvPaceket(self):
            print('---------------------------')
            print('Server otrzymal:')
            recvPakcet = findall('(.*?)\^', self.allPacket)
            for i in recvPakcet:
                print(i)
            print('---------------------------')
        def printSendPacket(self):
            print('+++++++++++++++++++++++++++')
            print('Server wysyla:')
            recvPakcet = findall('(.*?)\^', self.allPacket)
            for i in recvPakcet:
                print(i)
            print('+++++++++++++++++++++++++++')
#everthing what we recive we have to DEcode
        def recvPacket(self):
            #try:
               data = self.client.recv(1024)
               data = data.decode('ascii')
               recvPakcet=findall('>>(.*?)\^', data) # (.*?) oznacza niezachłanne dopasowanie znaków za wyjątkiem znaku 'n'.
               self.time = recvPakcet[0]
               self.operation = recvPakcet[1]
               self.liczb1 = recvPakcet[2]
               self.liczb2 = recvPakcet[3]
               self.liczb3 = recvPakcet[4]
               self.status = recvPakcet[5]
               self.clientID = recvPakcet[6]
               self.createAllPacket()
               self.printRecvPaceket()

            #except Exception:
             #           print("Blad podczas odczytywania pakietu")

        def getOperation(self):
            self.l1 = int(self.liczb1)
            self.l2 = int(self.liczb2)
            self.l3 = int(self.liczb3)
            if self.operation == 'op1':
                self.status=str(self.l1-self.l2-self.l3)
            if self.operation =='op2':
                self.status=str(self.l1/self.l2/self.l3)
            if self.operation == 'op3':
                self.status=str(self.l1+self.l2+self.l3)
            if self.operation == 'op4':
                self.status=str(self.l1*self.l2*self.l3)

# everything what we sendout we ENcode
        def sendPacket(self):
            self.time = time.ctime(time.time())
            self.clientID=str(self.id)
            self.getOperation()
            self.createAllPacket()
            self.client.send(self.allPacket.encode('ascii'))
            self.printSendPacket()



        def run(self):
            self.connection()
            self.recvPacket()
            self.sendPacket()
          #  self.recvPacket()
            #self.getOperation()
            #self.sendPacket()


def main():
    server = TCPServer()
    server.run()

if __name__=='__main__':
    main()








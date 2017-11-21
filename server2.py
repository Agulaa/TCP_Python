from socket import *
from threading import Lock, Thread
import time
from re import *
from allPacket import *

class Klient:
    def __init__(self, conn, adress,id):
        self.con=conn
        self.address=adress
        self.id=id


class TCPServer:

        def __init__(self):
            self.host = '127.0.0.1'
            self.port = 8080
            self.buffer = 1024
            self.threads = []
            self.id=0
            self.server = socket(AF_INET, SOCK_STREAM)
            self.client=''

        def connection(self):
            self.server.bind((self.host, self.port))
            print('Server binding socket')
            self.server.listen(5)
            while True:
                self.client, clientaddr = self.server.accept()
                self.id = self.id + 1
                ckli=Klient(self.client,clientaddr,self.id)
                print('Server polaczony  z ' +str(ckli.id))
                packet = allPacket()
                localtime = time.asctime(time.localtime(time.time()))
                identy = str(self.id)
                mesage=packet.encodePacket('', '', '', 'con', identy, '', localtime)
                print(packet.allMessage)
               # print(mesage) # jest z b'...'
                self.client.send(mesage)
            self.server.close()


        def recvPacketFromClientandSend(self):
               while True:
                   message=self.client.recv(self.buffer)
                   packet=allPacket()
                   print('es')
                   packet.decodePacket(message)
                   print(packet.allMessage)
                   try:
                       result = self.getOperation(packet)
                       print(result)
                       localtime = time.asctime(time.localtime(time.time()))
                       identy = str(self.id)
                       message=packet.encodePacket('', '', '', result[1], identy, result[0], localtime)
                       print("Serwer wysyla:" + packet.allMessage)
                       self.client.send(message)
                   finally:
                       self.client.close()





        def getOperation(self, packet):
            if  packet.liczb1 !='' and packet.liczb2 != '' and packet.liczb3 != '':
                if packet.operation == 'op1':
                     status=str(int(packet.liczb1)-int(packet.liczb2)-int(packet.liczb3))
                     operation = 'ok'
                     result=[status, operation]
                     return result


                if packet.operation =='op2':
                    if int(packet.liczb2) != 0 and int(packet.liczb3) !=0:
                         status=str(int(packet.liczb1)/int(packet.liczb2)/int(packet.liczb3))
                         operation = 'ok'
                         result = [status, operation]
                         return result
                    else:
                        operation='error'
                        status = ''
                        result = [status, operation]
                        return result

                if packet.operation == 'op3':
                     status = str(int(packet.liczb1)+int(packet.liczb2)+int(packet.liczb3))
                     operation = 'ok'
                     result = [status, operation]
                     return result
                if packet.operation == 'op4':
                     status=str(int(packet.liczb1)*int(packet.liczb2)*int(packet.liczb3))
                     operation = 'ok'
                     result = [status, operation]
                     return result
                else:
                    operation = 'error'
                    status = ''
                    result = [status, operation]
                    return result
            else:
               operation = 'error'
               status=''
               result = [status, operation]
               return result

# everything what we sendout we ENcode


        def run(self):
            self.connection()
            self.recvPacketFromClientandSend()



def main():
    server = TCPServer()
    server.run()

if __name__=='__main__':
    main()








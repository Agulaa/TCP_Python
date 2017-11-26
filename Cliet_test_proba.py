from socket import *
from ProtocolTest import *
import threading


class TCPClientT:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8878
        self.buffer = 1024
        self.identSe = ''
        self.socket = socket(AF_INET, SOCK_STREAM)

    def GetOperationAndNumbers(self):
        op = input('Choose operation ["op1"(-) ,"op2" (/),"op3" (*),"op4" (+)')
        one = input('First argument ')
        two = input('Second2 argument ')
        three = input('Theard 3 argument ')
        result = [op, one, two, three]
        return result

    def sendPacketToServer(self):
        protocol = ProtocolT()
        result = self.GetOperationAndNumbers()
        localtime = time.asctime(time.localtime(time.time()))
        message = protocol.encodeMessageToServer(result[1], result[2], result[3], result[0], self.identSe, 'WANT RESULT',
                                                 localtime)
        self.socket.send(message)
        print('Client send: ')
        print(protocol.allMessage)

    def answerFromServer(self):
        protocol = ProtocolT()
        message = self.socket.recv(self.buffer)

        # protocol.decodeProtocol(message)
        protocol.decodeMessageFromServertSecond(message)
        print('All message from server : ')
        print(protocol.allMessage)
        if protocol.status == 'OK':
            print('The operation on three arguments was done correctly')
            question = input('Do you want do more operation? Y/N')
            if question == 'y' or question == 'Y':
                self.continueSendPacketToServer()
            elif question == 'N' or question == 'n':
                localtime = time.asctime(time.localtime(time.time()))
                message = protocol.enconeMessageToClientFirstOrLast('DISCONNECT', str(protocol.identy), 'WANT',
                                                                    localtime)
                self.socket.send(message)
                print('Client want disconnect with server:')
                print(protocol.allMessage)
                self.socket.close()
            else:
                print('Wrong answer')
                exit()
        elif protocol.status == 'WRONG':
            print('The operation on three arguments was done wrong')
            question = input('Do you want do more operation? Y/N')
            if question == 'y' or question == 'Y':
                self.continueSendPacketToServer()
            elif question == 'N' or question == 'n':
                localtime = time.asctime(time.localtime(time.time()))
                message = protocol.enconeMessageToClientFirstOrLast('DISCONNECT', str(protocol.identy), 'WANT',
                                                                    localtime)
                self.socket.send(message)
                print('Client want disconnect with server')
                self.socket.close()
            else:
                print('Wrong answer')
                exit()
        else:
            print('Error from servwe')
            self.socket.close()




    def connAndRecvFromServer(self):
        self.socket.connect((self.host, self.port))
        # uzgodnienie identyfikaytora sesji
        protocol = ProtocolT()
        localtime = time.asctime(time.localtime(time.time()))
        messageFirst=protocol.encodeMessageToServerToWantIdenty('WANT ID', 'QUESTION', localtime, 'DONT HAVE')
        self.socket.send(messageFirst)
        message = self.socket.recv(self.buffer)
        # protocol.decodeProtocol(message)
        protocol.decodeMessageFromServerFirts(message)
        self.identSe = protocol.identy
        print('Client connect with  server, ID sesssion ID ' + str(protocol.identy))
        print('All Message form server : ')
        print(protocol.allMessage)
        client_threadS = threading.Thread(target=self.sendPacketToServer, args=())
        client_threadS.start()
        client_threadR = threading.Thread(target=self.answerFromServer, args=())
        client_threadR.start()

    def continueSendPacketToServer(self):
        client_threadS = threading.Thread(target=self.sendPacketToServer, args=())
        client_threadS.start()
        client_threadR = threading.Thread(target=self.answerFromServer, args=())
        client_threadR.start()

    def run(self):
        question = input('Do you want connect with server? (Y/N)')
        if question == 'Y' or question == 'y':
            self.connAndRecvFromServer()
        else:
            exit(1)


def Main():
    client = TCPClientT()
    client.run()


if __name__ == '__main__':
    Main()




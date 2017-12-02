from socket import *
from Protocol import *
import threading


class TCPClient:
    def __init__(self):
        self.host = '192.168.0.1'
        self.port = 8878
        self.buffer = 1024
        self.identSe = ''
        self.socket = socket(AF_INET, SOCK_STREAM)

    def GetOperationAndNumbers(self):
        """Metoda ktora pobiera operację od uźytkownika oraz 3 argumenty"""
        op = input('Choose operation ["op1"(-) ,"op2" (/),"op3" (*),"op4" (+)')
        one = input('First argument ')
        two = input('Second argument ')
        three = input('Third 3 argument ')
        result = [op, one, two, three]
        return result

    def sendPacketToServer(self):
        """Metoda, ktora wysyła wiadomość z operacją oraz z liczbamu"""
        protocol = Protocol()
        result = self.GetOperationAndNumbers()
        localtime = time.asctime(time.localtime(time.time()))
        message = protocol.encodeMessageToServer(result[1], result[2], result[3], result[0], self.identSe, 'WANTRESULT',localtime) #zakodowanie wiadomości z liczbami, operacją, swoim identyfikatorem, statusem 'WANTRESULT' aktulanym czasem
        self.socket.send(message) #wysyłanie wiadomości do servera
        print('Client send: ')
        print(protocol.allMessage)

    def answerFromServer(self):
        protocol = Protocol()
        message = self.socket.recv(self.buffer) #odenranie wiadomości od serwera

        # protocol.decodeProtocol(message)
        protocol.decodeMessageFromServertSecond(message) #odkodowanie wiadomości
        print('All message from server : ')
        print(protocol.allMessage)
        if protocol.status == 'OK':
            print('The operation on three arguments was done correctly')
            question = input('Do you want do more operation? Y/N')
            if question == 'y' or question == 'Y':
                self.continueSendPacketToServer()
            elif question == 'N' or question == 'n':
                localtime = time.asctime(time.localtime(time.time()))
                message = protocol.encodeMessageToServerToWantIdentyOrDsiconnect('DISCONNECT',  'WANT',localtime,str(protocol.identy),) #zakodowanie wiadmości z informacją, żeby zakończyć połączenie
                self.socket.send(message) #wysłanie wiadomości
                print('Client want disconnect with server:')
                print(protocol.allMessage)
                self.socket.close() #zamknięcie socketu
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
                message = protocol.encodeMessageToServerToWantIdentyorDsiconnect('DISCONNECT',  'WANT',localtime,str(protocol.identy))
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
        """Metoda ktora łączy się z klienyem i urchamia wątkek do wysłania i odebrania wiadomości od serwera"""
        self.socket.connect((self.host, self.port)) #połączenie się z hostem i portem
        # uzgodnienie identyfikaytora sesji
        protocol = Protocol()
        localtime = time.asctime(time.localtime(time.time()))
        messageFirst=protocol.encodeMessageToServerToWantIdentyOrDsiconnect('WANTID', 'QUESTION', localtime, 'DONTHAVE') #zakodowanie wiadomości z operacją 'WANTID', statusem 'QUESTION', czasem aktualnym, oraz identyfikatorem 'DONTHAVE'
        print(protocol.allMessage)
        self.socket.send(messageFirst) #wysłanie wiadomości do serwera
        message = self.socket.recv(self.buffer) #odebranie wiadomości od serwera
        protocol.decodeMesgageFromClientIDENTY(message) #odkodowanie wiadomości
        self.identSe = protocol.identy
        print('Client connect with  server, ID sesssion ID ' + str(protocol.identy))
        print('All Message form server : ')
        print(protocol.allMessage)
        client_threadS = threading.Thread(target=self.sendPacketToServer, args=()) #uruchomienie wątku dla wysłania pakietów
        client_threadS.start()
        client_threadR = threading.Thread(target=self.answerFromServer, args=()) #uruchomienie wątku dla odbieranie wiadmości od serwera
        client_threadR.start()

    def continueSendPacketToServer(self):
        """Metoda która wywołuje wątki, do kontynuacji wykonywania operacji na liczbach"""
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
    client = TCPClient()
    client.run()


if __name__ == '__main__':
    Main()




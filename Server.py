from socket import *
import threading
from Protocol import *


class TCPServer:

        def __init__(self):
            self.host = '192.168.0.1'
            self.port = 8878
            self.buffer = 1024
            self.ide = 0
            self.id = []
            self.freeID=[]
            self.counter = 0
            self.server = socket(AF_INET, SOCK_STREAM) # uwtorzenie gniazda TCP(IPv4, dane przesyłane strumieniowo)



        def connection(self):
            """Metoda która służy, do połączenia się z klientem oraz wysłania mu identyfikatora sesji """
            self.server.bind((self.host, self.port)) #przypisanie gniazdu do adresu iIP i portu
            print('Server started! Waiting for connections...')
            self.server.listen() #nasłuchiwanie nadchodzących połączeń

            while True:
                csocket, addres = self.server.accept() #akceptacja klienta
                messageFirst =csocket.recv(self.buffer)
                protocol = Protocol() #uwtorzenie obiektu, dzieki któremu będziemy mogli odkodować lub zakodować dane wysyłane podczas komunikacji pomędzi klientem a serwerem
                protocol.decodeMesgageFromClientIDENTY(messageFirst) #odkodowanie wiadomosci od serwera
                if protocol.operation=='WANTID': #sprawdzenie czy na pewno komunikat, ktory został wysłany przez klienta jest komunikatem do uzyskania identyfikatora sesji
                    print('Client '+str(addres)+ 'want ID from server') # wyświetlenie wiadomosci odebranej
                    print(protocol.allMessage)
                    if len(self.freeID) >0: #sprawdzenie czy są jakieś wolne ID w sewerze, jeśli nie to tworzony jest nowy ID sesji i wysyłane do klienta
                        self.id.append(self.freeID[-1])
                        del(self.freeID[-1])
                    else:
                        self.ide=self.ide +1
                        self.id.append(self.ide)
                    print('Server connected with client:' + str(self.id[-1]))
                    localtime = time.asctime(time.localtime(time.time())) #przypisanie do zmiennej aktualnego czasu
                    identy = str(self.id[-1]) #identyfikator klienta
                    message = protocol.encodeMessageToServerToWantIdentyOrDsiconnect('CONNECT', 'REPLY',localtime, identy) #zakodowanie wiadomości do klienta, z operacją 'CONNECT', identyfikatorem sesji, statusem 'REPLY' oraz aktualny czas
                    csocket.send(message) #wyslanie wiadomosci do klienta
                    print('Server send message with sessionID to client:')
                    print(protocol.allMessage) #wyswietlenie wiadomosci, ktora serwer wysyła
                    client_thread = threading.Thread(target=self.recvMessageFromClientandSend, args=(csocket,)) #uruchomienie wątku z fukcją, która pobiera liczby i wykonuje na nich operacje
                    client_thread.start()
                else:
                    print('UNKNOW OPERATION')






        def recvMessageFromClientandSend(self, csocket):
            """Metoda która odbiera wiadomosci od klienta, odczytuje z niej operację oraz trzy liczby, na których ma wykonać daną operację,
                a następnie ją wykonuje i tworzy pakiet z wynikiem i wysyła go do klienta"""
            try:
                while True:
                    try:
                        # everything what we recv  we DEcode
                        message = csocket.recv(self.buffer)  #odebranie wiadomosci od klienta
                        if not message:
                           break
                        protocol = Protocol()
                        protocol.decodeMessageFromClient(message) #odkodowanie wiadomosci
                        if protocol.operation == 'DISCONNECT': #jesli operacja jest 'DISCONNECT' to kończy połączenie z klientem
                            print('Server receive: ')
                            print(protocol.allMessage) #wyswietlenie wiadomosci od klienta
                            print('Client with ID ' + str(protocol.identy) + ' disconnect')
                            self.freeID.append(protocol.identy) #dodanie wolnego identyfikatora do tablicy wolnych ID
                            break
                        print('Server receive: ')
                        print(protocol.allMessage) # wyswietlenie wiadomosci
                        result = self.getOperation(protocol) #pobranie operacji, wyniku, oraz statusu
                        localtime = time.asctime(time.localtime(time.time())) #przypisanie do zmiennej aktualnego czasu
                       #everything what we send we ENcode
                        message = protocol.encodeMessageToClientWithResult('RESULT', str(protocol.identy),result[2], localtime, result[0] ) #zakodowanie wiadomosci z operacją 'RESULT', identyfikatorem sesji,
                        print("Server send to klient with ID " + str(protocol.identy) +' pakcket :')
                        print(protocol.allMessage)
                        csocket.send(message)#wysłanie wiadomosci do klienta
                    except KeyError:
                        exit()

            except ConnectionResetError:
                print('Client'+str(protocol.identy) +' disconnect')
                self.freeID.append(protocol.identy)




        def getOperation(self, protocol):
                  """Metoda która odczytuje operację oraz trzy liczby, następnie wykonuje na nich operację oraz zwraca wynik, oraz status operacji"""

                  one = int(protocol.liczb1)
                  two = int(protocol.liczb2)
                  tree = int(protocol.liczb3)

                  if protocol.operation == 'op1':
                      wynInt=one - two - tree
                      wynik=str(wynInt)
                      status = 'OK'
                      result=[wynik, protocol.operation, status]
                      return result

                  elif protocol.operation == 'op2':
                      if two != 0 and tree != 0:
                          wynInt = one / two / tree
                          wynik = str(wynInt)
                          status = 'OK'
                          result = [wynik, protocol.operation, status]
                          return result
                      else:
                         status = 'WRONG'
                         wynik = 'ERROR'
                         result = [wynik, protocol.operation , status]
                         return result

                  elif protocol.operation == 'op3':
                       wynInt = one * two * tree
                       wynik = str(wynInt)
                       status = 'OK'
                       result = [wynik, protocol.operation, status]
                       return result
                  if protocol.operation == 'op4':
                       wynInt = one + two + tree
                       wynik = str(wynInt)
                       status = 'OK'
                       result = [wynik, protocol.operation, status]
                       return result
                  else:
                     status = 'WRONG'
                     wynik = 'ERROR'
                     result = [wynik, protocol.operation, status]
                     return result




        def run(self):
            self.connection()




def main():
    server = TCPServer()
    server.run()

if __name__=='__main__':
    main()








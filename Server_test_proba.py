from socket import *
import threading
from ProtocolTest import *


class TCPServerT:

        def __init__(self):
            self.host = '127.0.0.1'
            self.port = 8878
            self.buffer = 1024
            self.id = []
            self.counter = 0
            self.server = socket(AF_INET, SOCK_STREAM)



        def connection(self):
            self.server.bind((self.host, self.port))
            print('Server started! Waiting for connections...')
            self.server.listen(4)

            while True:
                csocket, addres = self.server.accept()
                messageFirst =csocket.recv(self.buffer)

                protocol = ProtocolT()
                protocol.decodeMesgageFromClientIDENTY(messageFirst)
                if protocol.operation=='WANT ID':
                    print('Client '+str(addres)+ 'want ID from server')
                    print(protocol.allMessage)
                    self.counter = self.counter + 1
                    self.id.append(self.counter)
                    print('Server connected with client:' + str(self.id[-1]))
                    localtime = time.asctime(time.localtime(time.time()))
                    identy = str(self.id[-1])
                    message = protocol.enconeMessageToClientFirstOrLast('CONNECT',identy, 'REQUEST',localtime)
                    csocket.send(message)
                    print('Server send message with sessionID to client:')
                    print(protocol.allMessage)
                    client_thread = threading.Thread(target=self.recvMessageFromClientandSend, args=(csocket,))
                    client_thread.start()
                else:
                    print('UNKNOW OPERATION')
            #self.server.close()




        def recvMessageFromClientandSend(self, csocket):
            try:
                while True:
                    try:
                        # everything what we recv  we DEcode
                        message = csocket.recv(self.buffer)
                        if not message:
                           break
                        protocol = ProtocolT()
                        protocol.decodeMessageFromClient(message)
                        print('Server receive: ')
                        print(protocol.allMessage)
                        result = self.getOperation(protocol)
                        localtime = time.asctime(time.localtime(time.time()))
                       #everything what we send we ENcode
                        message = protocol.encodeMessageToClientWithResult('RESULT', str(protocol.identy),result[2], localtime, result[0] )
                        print("Server send to klient with ID " + str(protocol.identy) +' pakcket :')
                        print(protocol.allMessage)
                        csocket.send(message)
                    except KeyError:
                        exit()

            except ConnectionResetError:
                print('Client'+str(protocol.identy) +' disconnect')
                self.counter = self.counter - 1




        def getOperation(self, protocol):
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
    server = TCPServerT()
    server.run()

if __name__=='__main__':
    main()








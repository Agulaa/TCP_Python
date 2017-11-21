import time
from re import *

class allPacket:


    def __init__(self):
        self.time = ''
        self.operation = ''
        self.liczb1 = ''
        self.liczb2 = ''
        self.liczb3 = ''
        self.status = ''
        self.identy = ''
        self.allMessage = ''
        self.data=[]

    def cerateAllPacket(self):
        self.allMessage = "CzasKm>>" + self.time + "^OperaC>>" + self.operation + "^Liczb1>>" + self.liczb1 + "^Liczb2>>" + self.liczb2 + "^Liczb3>>" + self.liczb3 + "^StatuS>>" + self.status + "^IdentY>>" + self.identy + "^"

    def printAllPacket(self):
        packet = findall('>>(.*?)\^', self.allMessage)   # (.*?) oznacza niezachłanne dopasowanie znaków za wyjątkiem znaku 'n'.
        for i in packet:
            print(i)

    def encodePacket(self, num1, num2, num3, op, id, stat, tim):
        if num1 !='':
            self.liczb1 = str(num1)
            self.liczb2 = str(num2)
            self.liczb3 = str(num3)
        self.operation = op
        self.identy = id
        if stat != '':
             self.status = str(stat)
        self.time = tim
        self.cerateAllPacket()
        message=self.allMessage.encode('utf-8')
        return message

    def decodePacket(self, message):
        self.allMessage = message
        decMessage = self.allMessage.decode('utf-8')
        self.data = findall('>>(.*?)\^', decMessage)
        self.time = self.data[0]
        self.operation = self.data[1]
        self.liczb1 = self.data[2]
        self.liczb2 = self.data[3]
        self.liczb3 = self.data[4]
        self.status = self.data[5]
        self.identy = self.data[6]
        self.cerateAllPacket()








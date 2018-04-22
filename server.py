import multiprocessing
import socket
import os
import sys
import threading
import configparser
import json

dict = {'python': 'py', 'c++': 'cpp'}

def onSaveJsonInFile():
    process = multiprocessing.Process(target = saveJson)
    process.start()

def saveJson():
    jsonTest = json.dumps(dict)
    file = open('data.json', 'w')
    file.write(jsonTest)
    file.close()

def readFile():
    file = open('data.json', 'r')
    jsonTeste = json.load(file)
    print(jsonTeste)

onSaveJsonInFile()


def initializeThreads(newstdin):
    initReceiverThread(serverAddressPort)
    # initRecipientThread()
    # initPersistenceThread()
    # initResponseThread()

def initReceiverThread(serverAddressPort):
    process = multiprocessing.Process(target = receiverThread, args = (serverAddressPort, ))
    jobs.append(process)

def receiverThread(serverAddressPort):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind(serverAddressPort)
    while True:
        (data, addr) = s.recvfrom(bufferSize)
        print(data)

config = configparser.ConfigParser()
config.read('./settings.ini')

serverAddressPort   = (str(config.get('SERVER', 'host')), int(config.get('SERVER', 'port')))
bufferSize          = int(config.get('SERVER', 'packetBytes'))
jobs                = []

def main():
    newstdin = os.fdopen(os.dup(sys.stdin.fileno()))
    initializeThreads(newstdin)

    for j in jobs:
        j.start()

    for j in jobs:
        j.join()

if __name__ == '__main__':
    main()

# Listen for incoming datagrams
# while(True):
#     bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
#     message = bytesAddressPair[0]
#     address = bytesAddressPair[1]
#     clientMsg = "Message from Client:{}".format(message)
#     clientIP  = "Client IP Address:{}".format(address)

#     print(clientMsg)
#     print(clientIP)

#     # Sending a reply to client
#     UDPServerSocket.sendto(bytesToSend, address)
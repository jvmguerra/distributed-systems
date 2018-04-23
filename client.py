import multiprocessing
import socket
import os
import sys
import threading
import configparser
import json
import time

def initializeThreads(newstdin):
    initializeCommandThread(newstdin)
    initializeDisplayThread()

def initializeCommandThread(newstdin):
    process = multiprocessing.Process(target = sendCommand, args = (newstdin, ))
    jobs.append(process)

def initializeDisplayThread():
    process = multiprocessing.Process(target = receiveCommand, args = ())
    jobs.append(process)

def sendCommand(newstdin):
    sys.stdin = newstdin
    while True:
        try:
            message = ''
            time.sleep(.1)
            command = raw_input('Qual comando deseja realizar? (1: C, 2: R, 3: U, 4: D): ')
            mapItem = raw_input('Item que deseja realizar a operacao: ')
            if validator(command, mapItem):
                if (int(command) == 1 or int(command) == 3):
                    message = raw_input('String: ')
                jsonItem = {
                    'command': command,
                    'item': mapItem,
                    'string': message
                }
                UDPClientSocket.sendto(str.encode(json.dumps(jsonItem)), serverAddressPort)
            else:
                print('Dados Invalidos')
        except EOFError:
            return

def validator(command, mapItem):
    try:
        if (int(command) >= 1 and int(command) <=4 and int(mapItem)):
            return True
    except:
        return False

def receiveCommand():
    while True:
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        msg = "\nMessage from Server: {}".format(msgFromServer[0])
        print(msg)

config              = configparser.ConfigParser()
config.read('./settings.ini')
serverAddressPort   = (str(config.get('SERVER', 'host')), int(config.get('SERVER', 'port')))
bufferSize          = int(config.get('SERVER', 'packetBytes'))
UDPClientSocket     = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
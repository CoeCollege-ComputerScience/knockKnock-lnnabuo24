#from socket import *
from netTools import *

portNum = 2603

def simpleClient(host):
    s = socket()
    s.connect((host, portNum))
    data = receiveMessage(s)
    if data:
        print("initial: " + data)

    #msg = "\t" + input("prompt: ")
    sendMessage(s, "\tWho's there?")
    received = receiveMessage(s)
    print("received: " + received)
    msg = "\t" + input("prompt: ")
    while msg != "":
        sendMessage(s, msg)
        data = receiveMessage(s)
        print("response: " + data)
        msg = "\t" + input("prompt: ")
    print("closed connection")
    s.close()

#whatIP = input("give me an ip: ")
whatIP = getMyIP()

simpleClient( whatIP )


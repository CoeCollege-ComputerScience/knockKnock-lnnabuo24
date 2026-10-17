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

def generalizedKnockKnockClient(host):
    s = socket()
    s.connect((host, portNum))
    msg = input("HEAR or TELL (case insensitive): ")
    sendMessage(s, msg.upper())

    received = receiveMessage(s)
    print("response: " + received)
    while received != "Protocol Violation" and received != "":
        #print("gah")
        msg = input("prompt: ")
        check = input("add a \\t? (Y or N, default N) ")
        if check.lower() == "y":
            msg = "\t" + msg
        sendMessage(s, msg)
        received = receiveMessage(s)
        print("response: " + received)
    print("closed connection")
    s.close()

#whatIP = input("give me an ip: ")
#whatIP = getMyIP()

#name = input("give me a name: ")
#whatIP, status = mockDNSLookUp(name)
#whatIP, status = "192.168.0.225", "yeah fine" # <- hughes
whatIP, status = getMyIP(), "okayish"
print(whatIP + " " + status)

if status == "unknown":
    print("cant find them")
else:
    #simpleClient( whatIP )
    generalizedKnockKnockClient(whatIP)


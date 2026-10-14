#from socket import *
import datetime
import random

from netTools import *



jokes = []
fid = open("jokes.txt", "r")
for line in fid:
    newJoke = line.strip().split(" | ")
    print(newJoke)
    jokes.append( newJoke )
fid.close()

recentlySent = True
recentData = ""


def sendAMessage(socket, message):
    sendMessage(socket, message)

    global recentData
    global recentlySent
    recentlySent = True
    recentData = message
    print(recentData)

def receiveAMessage(socket):
    data = receiveMessage(socket)

    global recentData
    global recentlySent
    recentlySent = False
    recentData = data
    print(data)
    return data

def sendError(socket):
    #sendMessage(socket, "error: terrible at knock-knock jokes ")
    sendAMessage(socket, "error: terrible at knock-knock jokes")
    #socket.close()


def simpleServer():
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
    ip = getMyIP()
    #ip = "127.0.0.1"
    print(ip)
    s.bind((ip, 2603))
    s.listen()

    isFirstOpen = True

    while True:
        print("Waiting")
        conn, addr = s.accept()

        if isFirstOpen == True:
            # first time opened
            print("connected, first open")
            isFirstOpen = False
        else:
            print("connected, not the first open")
            if recentlySent:
                # its last action was to send data
                print("recent sent message: " + recentData)
            else:
                # it last received data
                print("recent received message: " + recentData)

        print(f"Connected by {addr}")
        #print(conn)

        #sentData = conn.recv(1024).decode("utf-8").lower()
        #sentData = receiveMessage(conn)

        sendAMessage(conn, "Knock-Knock")
        received = receiveAMessage(conn)
        whichJoke = jokes[ random.randint(0, len(jokes) - 1) ]
        #print(whichJoke)

        if received == "\tWho's there?":
            sendAMessage(conn, whichJoke[0])

            received = receiveAMessage(conn)
            if received == "\t" + whichJoke[0] + " who?":
                sendAMessage(conn, whichJoke[1])
                #conn.close()
            else:
                sendError(conn)
                #print("JAKJAJKS")

        else:
            sendError(conn)
            #print("i heard " + received)

        conn.close()

simpleServer()
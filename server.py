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
isFirstOpen = True


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

def beginBanana(conn):
    print("banana time")
    sendAMessage(conn, "Banana")
    received = receiveAMessage(conn)
    while received == "\tBanana who?":
        sendAMessage(conn, "Banana")
        received = receiveAMessage(conn)
    
    # loop ended, so they didnt send banana who
    if received == "\tBanana WHO!?":
        # finish the joke
        
        # hmmmmm
        # this feels weird
        # i didnt copy and paste this
        # but its really just the standard knock knock protocol
        # hmmmmmmm
        """
        what im thinking is basically
        the server sends banana
        it goes through the whole "banana who" stuff
        it then returns back to the standard knock-knock protocol
        """
        sendAMessage(conn, "Orange")
        received = receiveAMessage(conn)
        if received == "\tOrange who?":
            sendAMessage(conn, "Orange you glad I didn't say Banana")
        else:
            sendError(conn)
        #conn.close()
    else:
        # sent the wrong thing
        sendError(conn)

def processRequest(conn):

    global isFirstOpen
    global recentlySent
    global recentData

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

    sendAMessage(conn, "Knock-Knock")
    received = receiveAMessage(conn)
    whichJoke = jokes[random.randint(0, len(jokes) - 1)]
    # print(whichJoke)

    if received == "\tWho's there?":
        sendAMessage(conn, whichJoke[0])

        received = receiveAMessage(conn)
        if received == "\t" + whichJoke[0] + " who?":

            # right here
            if whichJoke[0] == "Banana":
                # the banana joke
                beginBanana(conn)
            else:
                # send the funny punchline
                sendAMessage(conn, whichJoke[1])
            # conn.close()
        else:
            sendError(conn)
            # print("JAKJAJKS")

    else:
        sendError(conn)
        # print("i heard " + received)
    conn.close()


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
        processRequest(conn)

simpleServer()

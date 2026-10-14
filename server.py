#from socket import *
import datetime
import random
import threading

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
    #sendAMessage(conn, "Banana")
    received = receiveAMessage(conn)
    print("got " + received)
    while received == "\tBanana who?":
        sendAMessage(conn, "Banana")
        received = receiveAMessage(conn)

    print("??? " + received)
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
        rather than implementing it again here
        """
        sendAMessage(conn, "Orange")
        return True
        #conn.close()

    # if this runs, they sent the wrong thing
    return False

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
    name = whichJoke[0]
    punchline = whichJoke[1]
    # print(whichJoke)

    if received == "\tWho's there?":
        sendAMessage(conn, name)

        #received = receiveAMessage(conn)

        wasBanana = False
        shouldContinue = True

        if name == "Banana":
            # sorry, my bad, right here
            wasBanana = True
            shouldContinue = beginBanana(conn)
            name = "Orange"
            # this feels a bit better
            # its like a small detour from the protocol

        received = receiveAMessage(conn)
        #print("are we ser " + received)

        # either it was *not* the banana joke and we got the correct response
        # or we began the banana joke and should continue
        #if ((not wasBanana) and received == "\t" + whichJoke[0] + " who?") or (wasBanana and shouldContinue):
        if (shouldContinue) and received == "\t" + name + " who?":

            sendAMessage(conn, punchline)
            """
            # oops
            # wrong spot
            if whichJoke[0] == "Banana":
                # the banana joke
                beginBanana(conn)
            else:
                # send the funny punchline
                sendAMessage(conn, whichJoke[1])
            """
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
        threading.Thread(target=processRequest, args=(conn,)).start()
        #processRequest(conn)

simpleServer()
#from socket import *
import datetime
import random
from threading import *

from netTools import *



jokes = []
fid = open("jokes.txt", "r")
for line in fid:
    newJoke = line.strip().split(" | ")
    print(newJoke)
    jokes.append( newJoke )
fid.close()


def sendAMessage(socket, message):
    sendMessage(socket, message)
    print("sent: " + message)

def receiveAMessage(socket):
    data = receiveMessage(socket)
    print("received: " + data)
    return data

def sendError(socket):
    #sendMessage(socket, "error: terrible at knock-knock jokes ")
    sendAMessage(socket, "error: terrible at knock-knock jokes")
    #socket.close()

def sendProtocolViolation(socket):
    sendAMessage(socket, "Protocol Violation")

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

def extendedKnockKnock_heardItAlready(conn):

    sendAMessage(conn, "Knock-Knock")
    received = receiveAMessage(conn)
    whichJoke = jokes[random.randint(0, len(jokes) - 1)]
    name = whichJoke[0]
    punchline = whichJoke[1]
    # print(whichJoke)

    if received == "\tWho's there?":
        sendAMessage(conn, name)

        #received = receiveAMessage(conn)

        #wasBanana = False
        shouldContinue = True

        if name == "Banana":
            # sorry, my bad, right here
            #wasBanana = True
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
            # send the funny punchline
            sendAMessage(conn, punchline)
        elif received == "I've heard that one already":
            sendAMessage(conn, "Ok, Sorry")
        else:
            sendError(conn)
            # print("JAKJAJKS")

    else:
        sendError(conn)
        # print("i heard " + received)
    #conn.close()

def generalizedProtocol(conn):
    received = receiveAMessage(conn)
    if received == "HEAR":
        # extended knock-knock protocol
        # (except if they heard it already)
        extendedKnockKnock_heardItAlready(conn)

        # it looks like this and the extended knock-knock protocol are separate things
        # possibly?
        # i know for this i should send Protocol Violation if the client deviates from this protocol
        # do i also send it if they deviate from the extended protocol
        # or do i stick with the error i have already
        # decisions decisions
    elif received == "TELL":
        # standard knock-knock protocol
        #
        # (except if they heard it already)
        sendAMessage(conn, "Ok, tell me a joke.")
        received = receiveAMessage(conn)
        if received == "Knock-Knock":
            sendAMessage(conn, "\tWho's there?")
            received = receiveAMessage(conn)
            # we now have the namae

            # now to find whether or not the server knows this joke already
            # pycharm why are you correcting my grammar
            # and capitalization
            alreadyExists = False
            for i in jokes:
                # i[0] is the name used in the joke
                # i[1] is the punchline
                if i[0] == received:
                    alreadyExists = True
                    break

            if alreadyExists:
                # heard this one before
                sendAMessage(conn, "I've heard that one already")
                received = receiveAMessage(conn)
                if received != "Ok, Sorry":
                    # even the final message can net you a protocol violation
                    sendProtocolViolation(conn)
            else:
                # havent heard this joke before
                sendAMessage(conn, received + " who?")
                received = receiveAMessage(conn)
                # we now have the punchline, how nice
                print("wow, that was a funny and original joke, i should add that to my jokes list")

        else:
            sendProtocolViolation(conn)
    conn.close()


def simpleServer():
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
    ip = getMyIP()
    #ip = "127.0.0.1"
    print(ip)
    s.bind((ip, 2603))
    s.listen()

    #myLock = Lock()

    while True:
        print("Waiting")
        conn, addr = s.accept()
        print(f'connected from {addr}')
        #Thread(target=processRequest, args=(conn,)).start()
        Thread(target=generalizedProtocol, args=(conn,)).start()
        #processRequest(conn)

simpleServer()
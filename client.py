#from socket import *
from netTools import *

portNum = 2603 # <- extended
#portNum = 2605 # <- generalized

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
    s.connect((host, 2605))
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



def tellAJoke_generalized(conn, name, punchline):
    sendMessage(conn, "Knock-Knock")
    received = receiveMessage(conn) # who's there
    sendMessage(conn, name) # <name>
    received = receiveMessage(conn) # <name> who (or heard this one)
    if received == "I've heard that one already":
        # heard this one
        print("i cannot believe they heard " + name + ", " + punchline + " before")
        sendMessage(conn, "Ok, Sorry")
    else:
        # <name> who
        print("yeah nobody expects the " + name + ", " + punchline)
        sendMessage(conn, punchline)

# i forgot a server would need to implement the generalized protocol
# in order to actually receive jokes
# so i made a tellAJoke function for a server that would follow the standard protocol if it was somehow told a joke
# oops
def shareJokesWithHost_generalized(host):

    jokes = []
    fid = open("jokes.txt", "r")
    for line in fid:
        newJoke = line.strip().split(" | ")
        print(newJoke)
        jokes.append(newJoke)
    fid.close()

    for item in jokes:
        s = socket()
        s.connect((host, 2605))
        sendMessage(s, "TELL")
        received = receiveMessage(s)
        tellAJoke_generalized(s, item[0], item[1])

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
    #shareJokesWithHost_generalized( whatIP )


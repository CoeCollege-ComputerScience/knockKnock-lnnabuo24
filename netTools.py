from socket import *


def sendMessage(socket, msg):
    socket.send(msg.encode("utf-8"))
    #socket.send(msg.encode("ascii"))

def receiveMessage(socket):
    data = socket.recv(1024).decode("utf-8")
    #data = socket.recv(1024).decode("ascii")
    return data

def receiveMessage_long(socket):
    data = socket.recv(1024)
    response = ""
    while data:
        response += data.decode("utf-8")
        data = socket.recv(1024)
    return response

def getMyIP():
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

mockDNSServerIP = "192.168.0.43"

def mockDNSLookUp(hostName):
    s = socket()
    #s.connect(("192.168.0.225", 2001))
    #s.connect(("192.168.0.43", 2001))
    s.connect((mockDNSServerIP, 2001))
    msg = hostName + "," + getMyIP()
    #s.send(msg.encode("utf-8"))
    #sendMessage(s, msg)
    s.send(msg.encode("ascii"))

    #response = s.recv(1024)
    #data = response.decode("utf-8")
    data = receiveMessage(s)
    #print(data)

    whatIP = ""
    whatStatus = ""

    status = data[3:]
    if status == "unsafe":
        raise ConnectionError("unsafe IP")
    else:
        nextMsg = "where " + hostName
        sendMessage(s, nextMsg)

        #result = receiveMessage(s)
        result = s.recv(1024).decode("ascii")
        #print(result)
        result = result.split(",")
        whatIP = result[0]
        whatStatus = result[1]

    s.close()

    if whatStatus == "unsafe":
        raise ConnectionError("unsafe IP")
    else:
        return whatIP, whatStatus



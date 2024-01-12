from socket import socket
from socket import AF_UNIX, SOCK_STREAM

SOCKET_ADDR = "/tmp/status.sock"

client = socket(AF_UNIX, SOCK_STREAM)


def openSocket():
    client.connect(SOCKET_ADDR)


def sendData(tag: str, data: any):
    # 发送的数据头部标题为tag内容为data
    print("tag:" + tag + " data:" + str(data))
    data = tag + ":" + str(data) + ";"
    client.send(data.encode("utf-8"))


def close():
    client.close()

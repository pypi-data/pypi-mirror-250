from socket import socket
from socket import AF_UNIX, SOCK_STREAM

SOCKET_ADDR = "/tmp/status.sock"

SOCKET_ADDR1 = "/tmp/position.sock"


class StatusSocket:
    def __init__(self):
        self.client = socket(AF_UNIX, SOCK_STREAM)
        self.client.connect(SOCKET_ADDR)

    def sendData(self, tag: str, data: any):
        # 发送的数据头部标题为tag内容为data
        data = tag + ":" + str(data) + ";"
        print("status_" + "tag:" + tag + " data:" + str(data) + ";")
        self.client.send(data.encode("utf-8"))

    def close(self):
        self.client.close()

    def __del__(self):
        self.close()


class PositionSocket:
    def __init__(self):
        self.client = socket(AF_UNIX, SOCK_STREAM)
        self.client.connect(SOCKET_ADDR1)

    def sendData(self, tag: str, data: any):
        # 发送的数据头部标题为tag内容为data
        data = tag + ":" + str(data) + ";"
        print("position_" + "tag:" + tag + " data:" + str(data) + ";")
        self.client.send(data.encode("utf-8"))

    def close(self):
        self.client.close()

    def __del__(self):
        self.close()

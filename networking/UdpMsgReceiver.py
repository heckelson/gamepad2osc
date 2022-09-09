from socket import socket, AF_INET, SOCK_DGRAM


class UdpMessageReceiver:
    """
    For debugging.
    """
    def __init__(self, port):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.port = port

    def listen_forever(self):
        print("Waiting for socket...")
        self.socket.bind(("", self.port))
        print(f"Socket bound to port {self.port}.")
        while True:
            data, addr = self.socket.recvfrom(1024)
            print(data)


if __name__ == "__main__":
    UdpMessageReceiver(9001).listen_forever()

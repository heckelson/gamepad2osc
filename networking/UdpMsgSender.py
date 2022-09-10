from socket import socket, AF_INET, SOCK_DGRAM


class UdpMsgSender:
    def __init__(self, hostname: str, port_num: int,
                 debug: bool = False):
        assert hostname is not None and \
               port_num is not None and \
               debug is not None

        self.hostname = hostname
        self.port_num = port_num
        self.debug = debug

        # create a UDP socket
        self.sock = socket(AF_INET, SOCK_DGRAM)

    def send_message(self, byte_message: bytearray):
        if self.debug:
            print(f"Sending message: {byte_message}")

        self.sock.sendto(byte_message, (self.hostname, self.port_num))

    def __del__(self):
        self.sock.close()

from socket import socket, AF_INET, SOCK_DGRAM


class UdpMsgSender:
    def __init__(self, hostname, port_num):
        self.hostname = hostname
        self.port_num = port_num

        # create a UDP socket
        self.sock = socket(AF_INET, SOCK_DGRAM)

    def send_message(self, byte_message: bytearray):
        debug = False
        if debug:
            print(f"Sending message: {byte_message}")

        self.sock.sendto(byte_message, (self.hostname, self.port_num))

    def __del__(self):
        self.sock.close()

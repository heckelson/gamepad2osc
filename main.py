import argparse as ap

from InputOscConverter import InputOSCConverter
from PS4GamepadManager import PS4GamepadManager
from networking.UdpMsgSender import UdpMsgSender

if __name__ == '__main__':
    # we need a hostname and a port
    parser = ap.ArgumentParser()
    parser.add_argument("hostname",
                        type=str,
                        help="the hostname you want to send the messages to,e.g. \"localhost\" or \"192.168.11.22\""
                        )
    parser.add_argument("port",
                        type=int,
                        help="the port you want to send the messages to, e.g. \"9001\"")

    args = parser.parse_args()

    hostname = args.hostname
    port_num = args.port
    sender = UdpMsgSender(hostname, port_num)

    mgr = PS4GamepadManager(InputOSCConverter("ps4"), sender)

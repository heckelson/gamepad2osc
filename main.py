import argparse as ap
from typing import Tuple

from InputOscConverter import InputOSCConverter
from PS4GamepadManager import PS4GamepadManager
from networking.UdpMsgSender import UdpMsgSender


def parse_args() -> Tuple[int, int]:
    """
    Parses the input args to get a target hostname and port to
    send OSC messages to.
    """
    parser = ap.ArgumentParser()
    parser.add_argument("hostname",
                        type=str,
                        help="the hostname you want to send the messages to, "
                             "e.g. \"localhost\" or \"192.168.11.22\""
                        )
    parser.add_argument("port",
                        type=int,
                        help="the port you want to send the messages to, "
                             "e.g. \"9001\"")

    args = parser.parse_args()

    _hostname = args.hostname
    _port_num = args.port

    return _hostname, _port_num


if __name__ == '__main__':
    hostname, port = parse_args()
    sender = UdpMsgSender(hostname, port)
    mgr = PS4GamepadManager(InputOSCConverter("ps4"), sender)

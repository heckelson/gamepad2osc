from pythonosc.osc_message_builder import OscMessageBuilder


class InputOSCConverter:
    """
    The InputOSCConverter object is created with a prefix such as "MyPs4Controller"
    or just "PS4", "XBOXONE", etc.
    To create a OSC message from an input, use that object's get_xxx_msg method.
    """

    def __init__(self, controller_prefix: str = "MyController"):
        self.prefix = controller_prefix

    def get_button_msg(self, button, status):
        assert button is not None and status is not None
        address = f"/{self.prefix}/button/{button}".lower().replace("-", "/")

        # create an OSC message object
        builder = OscMessageBuilder(address)
        builder.add_arg(status, 'i')
        msg = builder.build()

        return msg.dgram

    def get_axis_msg(self, axis, value):
        assert axis is not None and value is not None
        address = f"/{self.prefix}/axis/{axis}".lower().replace("-", "/")
        builder = OscMessageBuilder(address)
        builder.add_arg(value, 'f')
        msg = builder.build()

        return msg.dgram


# bad unit testing substitute but for now it's fine
if __name__ == '__main__':
    osc = InputOSCConverter("PS4")
    print(osc.get_button_msg("CROSS", 1))
    print(osc.get_axis_msg("LEFT_X", -0.887172))

from pythonosc.osc_message_builder import OscMessageBuilder


class InputOSCConverter:
    def __init__(self, controller_prefix: str):
        self.prefix = controller_prefix

    def get_button_msg(self, button, status):
        address = f"/{self.prefix}/button/{button}".lower().replace("-", "/")

        # create an OSC message object
        builder = OscMessageBuilder(address)
        builder.add_arg(status, 'i')
        msg = builder.build()

        return msg.dgram

    def get_axis_msg(self, axis, value):
        address = f"/{self.prefix}/axis/{axis}".lower().replace("-", "/")

        # create an OSC message object
        builder = OscMessageBuilder(address)
        builder.add_arg(value, 'f')
        msg = builder.build()

        return msg.dgram


# bad unit testing substitute but for now it's fine
if __name__ == '__main__':
    osc = InputOSCConverter("PS4")
    print(osc.get_button_msg("CROSS", 1))
    print(osc.get_axis_msg("LEFT_X", -0.887172))

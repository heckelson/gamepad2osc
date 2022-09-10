# gamepad2osc

This is a program plugging together `python-osc` and [Gamepad](https://github.com/piborg/Gamepad) in order to control music instruments in [PureData](https://puredata.info/).

## How to run

* Run `pipenv install` to install the packages in the Pipfile.
* Run `pipenv run python main.py <hostname> <port>` and plug in your Controller.

## Project Outline

`main.py` contains just the argparsing and then starts the PS4GamepadManager.

`InputOscConverter` is a helper class that uses Button/Axis inputs to format OSC messages.

`PS4GamepadManager` defines and registers callback functions for button presses which are converted and then sent out via the `UdpMsgSender`.


## Other Resources

[OSC Message format reference](http://wosclib.sourceforge.net/osc-ref.pdf)

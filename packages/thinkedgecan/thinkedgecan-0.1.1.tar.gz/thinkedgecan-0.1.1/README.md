This plugin adds support for the ThinkEdge SE50's CAN-bus controller to the [`python-can`][candocs] library.
Specifically, the ThinkEdge SE50 provides a CAN-bus connection via a SUNIX Industry card.

## System requirements

* Hardware: ThinkEdge SE50
* Operating system: Ubuntu 20.04 GA

## Installation

1. Download and unzip the drivers from [Lenovo][zip]
2. This folder contains a PDF with the name "SDC Expansion Board SDK Document1.0.2-linux.pdf". Follow the instructions inside the PDF to install the driver and to check the driver status. You can disregard all instructions that come after.
3. Run `pip install path/to/thinkedgecan`.


## Usage

Refer to the [documentation of `python-can`][candocs] for general usage.

Create the `Bus` object with the following code:

```python
from can import ThreadSafeBus

with ThreadSafeBus(interface="sunix", baudrate=500) as bus:
    ...
```

For the baudrate, you can choose one of 125, 250, 500 and 1000 kbit/s. All devices on a CAN-bus must use the same baudrate.

[candocs]: https://python-can.readthedocs.io/
[zip]: https://download.lenovo.com/consumer/iot/l1ind04s11avc_tese50.zip

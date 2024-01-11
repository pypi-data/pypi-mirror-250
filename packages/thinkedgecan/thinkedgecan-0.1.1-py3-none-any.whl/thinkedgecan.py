"""Ctypes wrapper for the CAN-bus of the SUNIX SDC Expansion board.

(c) 2023 - IFOS GmbH, Wesehof 29, 59757 Arnsberg, Germany

This is based on an SDK downloaded from:
https://download.lenovo.com/consumer/iot/l1ind04s11avc_tese50.zip
"""

from typing import Any, Callable, Literal, Optional

from ctypes import byref, c_int, c_ubyte, c_uint, cdll, Structure
from enum import IntEnum
from functools import wraps
import logging
import time
import warnings

from can import BusABC, Message
import can.typechecking

__version__ = "0.1.1"
__all__ = ["SunixBus"]

try:
    libsdcio = cdll.LoadLibrary("libsdcio.so")
except OSError as e:
    raise can.CanInterfaceNotImplementedError(
        "Could not load libsdcio.so. Make sure the driver is installed.",
        e.errno,
    )

logger = logging.getLogger("can.sunix")

Bitrate = Literal[125_000, 250_000, 500_000, 1_000_000]
BITRATE_CODES = {1_000_000: 0x01, 500_000: 0x02, 250_000: 0x03, 200_000: 0x04, 125_000: 0x05}

FrameFormat = Literal["standard", "extended"]
FRAME_FORMATS = {"standard": 0, "extended": 1}

CType = Any


class _CanInfo(Structure):
    # Source:
    # l1ind04s11avc_tese50.zip/L1IND04S11AVC/sdk.tar.gz/sdk/SDClib_V1.0.3.2.pdf
    # Section 5.1.2
    _fields_ = [
        ("bus_number", c_ubyte),
        ("device_number", c_ubyte),
        ("line", c_ubyte),
        ("access_address", c_uint),
        ("irq", c_ubyte),
        ("version", c_ubyte),
        ("frame_format", c_ubyte),
        ("rid", c_uint * 2),
        ("baudrate", c_ubyte),
    ]


class Return(IntEnum):
    C_FAILURE = -1
    SDCSPI_STATUS_SUCCESS = 0x0000
    SDCSPI_LENGTH_INVALID = 0x0001
    SDCSPI_DATA_INVALID = 0x0002
    SDCSPI_CONTROLLER_VERSION_UNSUPPORT = 0x0003
    SDCSPI_UNSUPPORT_COMMAND = 0x0004
    SDCSPI_ALLOC_MEMORY_FAIL = 0x0005
    SDCSPI_INVALID_LINE_NUM = 0x0006  # undocumented guess
    SDCSPI_NO_SUCH_FILE = 0x0007
    SDCSPI_PARAMETER_INVALID = 0x0009
    SDCSPI_DEVICE_BUSY = 0x0010
    SDCSPI_NOT_OPEN = 0x0011  # undocumented guess
    SDCSPI_STATUS_RX_TIMEOUT = 0x0023

    @classmethod
    def string(cls, error_code: int) -> str:
        try:
            return cls(error_code).name
        except ValueError:
            return "UNKNOWN_ERROR"


def _open(channel: int) -> None:
    """Open this CAN channel.

    :raises ~can.exceptions.CanInterfaceNotImplementedError:
        If the driver cannot be accessed
    :raises ~can.exceptions.CanInitializationError:
        If the bus cannot be initialized
    """
    res = libsdcio.sdc_can_open(channel)
    if res == Return.SDCSPI_STATUS_SUCCESS:
        return
    if res == Return.SDCSPI_DATA_INVALID and channel:
        raise can.CanInterfaceNotImplementedError(
            f"Channel {channel} could not be found. Try channel 0.",
            res,
        )
    raise can.CanInitializationError(
        f"Failed to open CAN-bus. {Return.string(res)}.",
        res,
    )


def _check(
    func: Callable[..., int], use_channel: bool = True
) -> Callable[..., None]:
    """Check for return values and format errors uniformly.

    :raises ~can.exceptions.CanError:
        If func returns nonzero.
    """

    @wraps(func)
    def wrapped(self: "SunixBus", *args: tuple[CType]) -> None:
        logger.debug(f"start {func.__name__}")
        if use_channel:
            args = (self.channel,) + args  # type: ignore
        res = func(*args)
        logger.debug(f"{func.__name__} returned {res}.")
        if res != Return.SDCSPI_STATUS_SUCCESS:
            raise can.CanOperationError(
                f"{Return.string(res)} returned by {func.__name__}.",
                res,
            )

    return wrapped


class SunixBus(BusABC):
    """Ctypes wrapper for the CAN-bus of the SUNIX SDC Expansion board."""

    _lib_set_baudrate = _check(libsdcio.sdc_can_set_baudrate)
    _lib_close = _check(libsdcio.sdc_can_close)
    _lib_get_info = _check(libsdcio.sdc_can_get_info, use_channel=False)
    _lib_write_data = _check(libsdcio.sdc_can_write_data)
    _lib_read_data = _check(libsdcio.sdc_can_read_data)
    _lib_set_accept_id = _check(libsdcio.sdc_can_set_accept_id)
    

    def __init__(
        self,
        channel: int = 0,
        can_filters: Optional[can.typechecking.CanFilters] = None,
        /,
        receive_format: Optional[FrameFormat] = None,
        bitrate: Bitrate = 500_000,  # bit/s
        **kwargs,
    ) -> None:
        """Open CAN channel

        :param channel:
            The can interface identifier.

        :param can_filters:
            See :meth:`~can.BusABC.set_filters` for details.

        :param receive_format:
            Receive only "standard" or "extended" frames.
            This parameter is required because the CAN driver cannot receive both.
            However, the frame format can be changed later with
            :meth:`~thinkedgecan.SunixBus.set_receive_format`.
            Regardless of this setting, standard and extended frames can be sent.

        :param bitrate:
            The bitrate of the bus in bit/s.
            Either 125 000, 250 000, 500 000 or 1 000 000.

        :raises ValueError:
            If parameters are out of range.
        :raises ~can.exceptions.CanInterfaceNotImplementedError:
            If the driver cannot be accessed.
        :raises ~can.exceptions.CanInitializationError:
            If the bus cannot be initialized.
        """
        channel = int(channel)
        self.channel = channel
        self.channel_info = f"SUNIX CAN-bus interface, channel {channel}"
        super().__init__(channel=channel, can_filter=can_filters, **kwargs)
        _open(channel)
        if receive_format is None:
            warnings.warn(
                "No frame format selected. "
                "Pass receive_format='standard' or receive_format='extended'! "
                "Setting to receive_format='standard'. "
                "Extended frames will be ignored."
            )
            receive_format = "standard"
        self.set_receive_format(receive_format)
        self._set_bitrate(bitrate)
        self._info = self._get_info()

    def shutdown(self):
        """Close the CAN bus."""
        try:
            self._lib_close(self.channel)
        except can.CanOperationError as e:
            if e.error_code != Return.SDCSPI_NO_SUCH_FILE:
                raise
        super().shutdown()

    def send(self, msg: Message, timeout: Optional[float] = None) -> None:
        """Send Message over the CAN-bus.

        :param Message:
            The message to send.

        :param timeout:
            This parameter is ignored.

        :raises ~can.exceptions.CanOperationError:
            If an error occurred while sending.
        """
        # TODO: What if `msg.dlc` differs from `len(msg.data)`?
        # TODO: Fix `tx is busy` stderr output. (Not required for Smart Forestry.)
        # A time.sleep call that's longer than the transmission time is not sufficient.
        if msg.data is None:
            raise ValueError("Cannot send a None value.")
        datalen = msg.dlc
        if not 1 <= datalen <= 8:
            raise ValueError(
                "The data must be at least 1 byte and at most 8 bytes long. "
                f"Received {datalen} bytes."
            )
        data = (c_ubyte * datalen)(*msg.data)
        self._lib_write_data(
            msg.arbitration_id,
            msg.is_extended_id,
            byref(data),
            datalen,
        )

    def _recv_internal(
        self, timeout: Optional[float] = 0
    ) -> tuple[Optional[Message], bool]:
        """Receive CAN message if there is one right now.

        :param timeout:
        This parameter is ignored.

        :return:
            1.  A message that was read or None on timeout.
            2.  False.

        :raises ~can.exceptions.CanOperationError:
            If an error occurred while reading.
        """
        self._lib_read_data(
            byref(rid := c_uint()),
            byref(frame_format := c_ubyte()),
            byref(data := (c_ubyte * 8)()),
            byref(datalen := c_int()),
        )
        msg = (
            Message(
                check=True,
                timestamp=time.time(),
                arbitration_id=rid.value,
                is_extended_id=bool(frame_format.value),
                # remote frame not indicated by SUNIX driver.
                # error frame ignored by SUNIX driver.
                channel=self.channel,
                dlc=datalen.value,
                data=data[: datalen.value],
                # FD not indicated by SUNIX driver.
                is_rx=True,
            )
            if datalen
            else None
        )
        return msg, False

    def _set_bitrate(self, bitrate: Bitrate) -> None:
        """Set bitrate on channel.

        :raises ValueError:
            If an invalid bitrate is passed.
        :raises ~can.exceptions.CanOperationError:
            If an error occurs while setting the bitrate.
        """
        try:
            code = BITRATE_CODES[bitrate]
        except KeyError:
            raise ValueError(
                f"The bitrate must be one of {list(BITRATE_CODES)}. "
                f"`{bitrate}` was supplied instead."
            )
        self._lib_set_baudrate(code)

    def _get_info(self) -> _CanInfo:
        """Return channel info.

        :raises ~can.exceptions.CanOperationError:
        """
        info = _CanInfo()
        self._lib_get_info(self.channel, byref(info))
        return info
    
    def set_receive_format(self, frame_format: FrameFormat) -> None:
        self._lib_set_accept_id(FRAME_FORMATS[frame_format], 0, 0)


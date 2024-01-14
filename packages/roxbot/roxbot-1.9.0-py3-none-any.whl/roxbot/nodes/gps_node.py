#!/usr/bin/env python3
"""
 node for Septentrio GPS receiver

 Copyright (c) 2023 ROX Automation - Jev Kuznetsov
"""

import asyncio
import logging
from enum import Enum, auto

import pynmea2  # type: ignore
import serial_asyncio  # type: ignore

from roxbot.interfaces import Pose


# enum for gps warnings
class FixProblem(Enum):
    """enum for gps warnings"""

    NONE = auto()
    INCOMPLETE_DATA = auto()
    NO_FIX = auto()
    OLD_FIX = auto()


class FixException(Exception):
    """exception for gps fix errors"""

    def __init__(self, reason: FixProblem):
        self.reason = reason

    def __str__(self):
        return f"GPS fix problem: {self.reason.name}"


class SSN(pynmea2.ProprietarySentence):
    """proprietary message definition"""

    fields = [
        ("no_desc", "_"),
        ("no_desc", "sentence_type"),
        ("no_desc", "timestamp"),
        ("no_desc", "date"),
        ("no_desc", "heading", float),
        ("no_desc", "roll"),
        ("no_desc", "pitch"),
        ("no_desc", "heading_stdev", float),
        ("no_desc", "roll_stdev"),
        ("no_desc", "pitch_stdev"),
        ("no_desc", "sats_used"),
        ("no_desc", "rtk_mode", int),
        ("no_desc", "magnetic_variation"),
        ("no_desc", "mag_var_direction"),
    ]


class GpsNode:
    """receive gps data from serial port, parse it an keep track of fix status"""

    def __init__(self, port: str, baudrate: int = 115_200):
        self._log = logging.getLogger(self.__class__.__name__)

        # position data
        self.lat = None
        self.lon = None
        self.gps_qual = None
        self.heading = None
        self.heading_stdev = None

        self._port = port
        self._baudrate = baudrate

        # number of received messages
        self.status = {"nmea_latlon": 0, "nmea_heading": 0, "imu": 0}

    async def _handle_nmea(self):
        """handle incoming nmea messages"""

        self._log.info(f"Connecting to gps on {self._port}")

        reader, _ = await serial_asyncio.open_serial_connection(
            url=self._port, baudrate=self._baudrate
        )

        while True:
            line = await reader.readline()
            txt = line.strip().decode()
            self._log.debug(txt)
            self.parse_nmea(txt)

    def parse_nmea(self, txt: str):
        """process nmea message"""
        if txt.startswith("$PSSN"):
            try:
                msg = pynmea2.parse(txt)
                self.heading = msg.heading
                self.heading_stdev = msg.heading_stdev

                self._log.debug(
                    "%s", f"heading: {self.heading}, stdev: {self.heading_stdev}"
                )

                self.status["nmea_heading"] += 1

            except Exception as e:  # pylint: disable=broad-except
                self._log.error("Error parsing PSSN message: %s", e)
            return

        if txt.startswith("$GPGGA"):
            try:
                msg = pynmea2.parse(txt)
                self.lat = msg.latitude
                self.lon = msg.longitude
                self.gps_qual = msg.gps_qual
                # rec["ts"] = msg.timestamp
                self._log.debug(
                    "%s", f"lat: {self.lat}, lon: {self.lon}, qual: {self.gps_qual}"
                )
                self.status["nmea_latlon"] += 1
            except Exception as e:  # pylint: disable=broad-except
                self._log.error("Error parsing GPGGA message: %s", e)

    def get_pose(self) -> Pose:
        """get current pose in meters (x,y,theta)"""

        # check that all data is available
        if self.lat is None or self.lon is None or self.heading is None:
            raise FixException(FixProblem.INCOMPLETE_DATA)

        return Pose.from_gps(self.lat, self.lon, self.heading)

    async def main(self):
        """main coroutine"""
        self._log.info("Starting gps node")
        await self._handle_nmea()


def demo(tty_port: str = "/dev/gps_nmea"):
    """demo gps messages"""

    node = GpsNode(port=tty_port)

    print("Receiving messages, press Ctrl-C to stop")
    try:
        asyncio.run(node.main())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    import coloredlogs  # type: ignore

    coloredlogs.install(
        level="DEBUG", fmt="%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s"
    )
    demo()

#!/usr/bin/env python3
"""
 Odometry classes

 Copyright (c) 2023 ROX Automation - Jev Kuznetsov
"""


from typing import Tuple
import math


class Odometer:
    """base odometry class, defining odometer interface"""

    def __init__(self) -> None:
        super().__init__()
        self._x: float = 0.0
        self._y: float = 0.0
        self._theta: float = 0.0

    def get_pose(self) -> Tuple[float, float, float]:
        """current pose"""
        return self._x, self._y, self._theta

    def set_pose(self, x: float, y: float, theta: float):
        """set current pose"""
        self._x = x
        self._y = y
        self._theta = theta


class DiffDriveOdometer(Odometer):
    """odometer for a differential drive robot"""

    def __init__(self, wheel_base: float, s_total: Tuple[float, float] = (0.0, 0.0)):
        super().__init__()
        self._W = wheel_base
        self._s_total = s_total

    def update(self, s_left: float, s_right: float) -> None:
        """update pose

        Args:
            s_left (float): distance traveled by left axle
            s_right (float): distance traveled by right axle
        """

        ds_l = s_left - self._s_total[0]
        ds_r = s_right - self._s_total[1]

        dst = (ds_l + ds_r) / 2

        self._x += dst * math.cos(self._theta)
        self._y += dst * math.sin(self._theta)

        self._theta += (ds_r - ds_l) / self._W

        self._s_total = (s_left, s_right)

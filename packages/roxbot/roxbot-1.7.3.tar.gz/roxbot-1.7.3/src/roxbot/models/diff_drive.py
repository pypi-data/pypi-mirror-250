#!/usr/bin/env python3
"""
 Differential drive robot model

 Copyright (c) 2024 ROX Automation - Jev Kuznetsov
"""

from typing import Tuple

from roxbot.vectors import Vector

from .wheels import Wheel


class DiffDriveModel:
    """basic differential drive robot model."""

    DEFAULT_WHEEL_BASE = 0.16
    DEFAULT_WHEEL_DIAMETER = 0.066
    DEFAULT_WHEEL_ACCEL = 1e6

    def __init__(
        self,
        wheel_base: float = DEFAULT_WHEEL_BASE,
        wheel_diameter: float = DEFAULT_WHEEL_DIAMETER,
        wheel_accel: float = DEFAULT_WHEEL_ACCEL,
    ):
        self.left_wheel = Wheel(wheel_diameter, wheel_accel)
        self.right_wheel = Wheel(wheel_diameter, wheel_accel)
        self._W = wheel_base  # wheel base width

        self.xy = Vector()  # position
        self.theta = 0.0  # orientation

        self.t = 0.0  # time counter

    @property
    def pose(self) -> Tuple[float, float, float]:
        return (self.xy.x, self.xy.y, self.theta)

    @property
    def vl(self) -> float:
        return self.left_wheel.velocity_ms

    @property
    def vr(self) -> float:
        return self.right_wheel.velocity_ms

    @property
    def v(self) -> float:
        """linear velocity in m/s"""
        return (self.vl + self.vr) / 2

    @property
    def omega(self) -> float:
        return (self.vr - self.vl) / self._W

    @property
    def curvature(self) -> float:
        """driving curvature"""
        try:
            return 1 / (0.5 * self._W * (self.vl + self.vr) / (self.vr - self.vl))
        except ZeroDivisionError:
            return 0.0

    def set_pose(self, x: float, y: float, theta: float):
        self.xy = Vector(x, y)
        self.theta = theta

    def set_vel(self, vl: float, vr: float):
        """set left and right target velocities"""

        self.left_wheel.set_velocity_ms(vl)
        self.right_wheel.set_velocity_ms(vr)

    def vc_to_vels(self, v: float, c: float) -> Tuple[float, float]:
        """convert vel/curvature to Vl, Vr

        Args:
            v (float): linear velocity
            c (float): curvature = 1/R

        Returns:
            Tuple[float,float]: Vl and Vr in m/s
        """

        if c == 0:
            return (v, v)

        R = 1 / c
        vr = (v * self._W + 2 * R * v) / 2 / R
        vl = 2 * v - vr

        return vl, vr

    def step(self, dt: float):
        """perform timestep"""

        self.left_wheel.step(dt)
        self.right_wheel.step(dt)

        # using a simple approximation, should be good enough for short dt
        # don't bother with icc...
        dxy = Vector.from_polar(self.v * dt, self.theta)
        self.xy += dxy

        self.theta += self.omega * dt

        self.t += dt

    def __repr__(self) -> str:
        return f"diffdrive vels: ({self.vl:.2f},{self.vr:.2f}) C={self.curvature}"

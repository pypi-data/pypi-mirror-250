#!/usr/bin/env python3
"""
 Differential drive robot model

 Copyright (c) 2024 ROX Automation - Jev Kuznetsov
"""

from typing import Tuple

from roxbot.vectors import Vector

from .wheels import Wheel
from .protocols import RobotModelProtocol


def vc_to_vels(v: float, c: float, W: float) -> Tuple[float, float]:
    """convert vel/curvature and wheelbase to Vl, Vr

    Args:
        v (float): linear velocity
        c (float): curvature = 1/R
        W (float): wheelbase

    Returns:
        Tuple[float,float]: Vl and Vr in m/s
    """

    if c == 0:
        return (v, v)

    R = 1 / c
    vr = (v * W + 2 * R * v) / 2 / R
    vl = 2 * v - vr

    return vl, vr


class DiffDriveModel(RobotModelProtocol):
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
        self.W = wheel_base  # wheel base width

        self.xy = Vector()  # position
        self.theta = 0.0  # orientation

        self.t = 0.0  # time counter

    @property
    def pose(self) -> Tuple[float, float, float]:
        return (self.xy.x, self.xy.y, self.theta)

    @pose.setter
    def pose(self, value: Tuple[float, float, float]) -> None:
        self.xy.x, self.xy.y, self.theta = value

    @property
    def vl(self) -> float:
        return self.left_wheel.velocity_ms

    @property
    def vr(self) -> float:
        return self.right_wheel.velocity_ms

    @property
    def velocity(self) -> float:
        """linear velocity in m/s"""
        return (self.vl + self.vr) / 2

    @property
    def omega(self) -> float:
        return (self.vr - self.vl) / self.W

    @property
    def curvature(self) -> float:
        """driving curvature"""
        try:
            return 1 / (0.5 * self.W * (self.vl + self.vr) / (self.vr - self.vl))
        except ZeroDivisionError:
            return 0.0

    def step(self, dt: float):
        """perform timestep"""

        self.left_wheel.step(dt)
        self.right_wheel.step(dt)

        # using a simple approximation, should be good enough for short dt
        # don't bother with icc...
        dxy = Vector.from_polar(self.velocity * dt, self.theta)
        self.xy += dxy

        self.theta += self.omega * dt

        self.t += dt

    def cmd_vel(
        self, linear_velocity: float, angular_velocity: float
    ) -> tuple[float, float]:
        """set wheel velocities from linear and angular velocities, returns calculated target velocities"""

        vl = linear_velocity - angular_velocity * self.W / 2
        vr = linear_velocity + angular_velocity * self.W / 2

        self.cmd_lr(vl, vr)
        return vl, vr

    def cmd_vc(self, linear_velocity: float, curvature: float) -> tuple[float, float]:
        """set wheel velocities from linear velocity and curvature"""

        vl, vr = vc_to_vels(linear_velocity, curvature, self.W)

        self.cmd_lr(vl, vr)
        return vl, vr

    def cmd_lr(self, left_velocity: float, right_velocity: float):
        """set wheel velocities from left and right velocities"""

        self.left_wheel.set_velocity_ms(left_velocity)
        self.right_wheel.set_velocity_ms(right_velocity)

    def __repr__(self) -> str:
        return f"diffdrive vels: ({self.vl:.2f},{self.vr:.2f}) C={self.curvature}"

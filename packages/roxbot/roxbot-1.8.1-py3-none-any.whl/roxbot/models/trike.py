#!/usr/bin/env python3
"""
 Kinematic for wheeled robots

 Copyright (c) 2023 ROX Automation - Jev Kuznetsov

 ## References

* https://www.cs.columbia.edu/~allen/F19/NOTES/icckinematics.pdf

**units** All units are SI (meters, radians, seconds), unless otherwise noted in variable names,
for example `anggle_deg` is in degrees.

**coordinate system** : the coordinate system is right handed, with the x-axis pointing forward,
the y-axis pointing to the left and the z-axis pointing up.

"""

import math
from typing import Optional, Tuple
from roxbot.vectors import Vector

from .wheels import Wheel
from .linear_model import LinearModel


class TrikeModel:
    """
    ## Kinematic model of a trike


    Trike model is a combination of a bycicle and and a differential drive kinematic models.

    Key features are:

    * the path curvature is governed by steering wheel
    * movement command interface is `(velocity,steering angle)`
    * differential speeds for the driving wheels are calculated from the driving curvature.


    !!! note
        The steering wheel axle can be behind driving wheels resulting in rear wheel steering
        To achieve this, use negative `L` value.


    ### Geometry

    !!! note
        Axes in Geogebra model are different from the ones used in this model.
        This model uses right handed coordinate system with x-axis pointing forward, y-axis pointing to the left and z-axis pointing up.

    <iframe src="https://www.geogebra.org/calculator/rea6w9a2?embed" width="800" height="800" allowfullscreen style="border: 1px solid #e4e4e4;border-radius: 4px;" frameborder="0"></iframe>


    """

    __slots__ = (
        "L",
        "B",
        "wheel_diameter",
        "left_wheel",
        "right_wheel",
        "wheels",
        "steer",
        "target_velocity",
        "xy",
        "theta",
        "time",
    )

    def __init__(
        self,
        L: float = 1.0,
        B: float = 0.8,
        wheel_diameter: float = 0.4,
        wheel_accel: float = 1.0,
        steer_speed: float = math.radians(10.0),
        max_velocity: Optional[float] = None,
    ) -> None:
        """create kinematic model of a trike

        Args:
            L (float, optional): length, distance between front and back axles. Defaults to 1.0.
            B (float, optional): wheel base. Defaults to 0.8.
            wheel_diameter (float, optional): Driving wheel diameter. Defaults to 0.4.
            wheel_accel (float, optional): Driving wheel acceleration [m/s2]. Defaults to 1.0.
            steer_speed (float, optional): Steering wheel speed [rad/s]. Defaults to 10.0 deg.
            max_velocity (Optional[float], optional): maximum wheel velocity [m/s]. Defaults to None.
        """

        self.L = L
        self.B = B
        self.wheel_diameter = wheel_diameter

        self.target_velocity: float = 0.0

        # define wheels
        self.left_wheel = Wheel(wheel_diameter, wheel_accel, max_velocity=max_velocity)
        self.right_wheel = Wheel(wheel_diameter, wheel_accel, max_velocity=max_velocity)
        self.wheels = [self.left_wheel, self.right_wheel]

        # steering wheel model
        self.steer = LinearModel(roc=steer_speed)

        # position
        self.xy = Vector()
        self.theta: float = 0.0

        # time
        self.time: float = 0.0

    @property
    def velocity(self) -> float:
        """actual velocity in m/s"""
        return (self.wheels[0].velocity_ms + self.wheels[1].velocity_ms) / 2

    @property
    def steering_angle(self) -> float:
        """steering angle in radians"""
        return self.steer.val

    @property
    def target_steer(self) -> float:
        """target steering angle in radians"""
        return self.steer.setpoint

    @target_steer.setter
    def target_steer(self, angle: float) -> None:
        """set target steering angle in radians"""
        self.steer.setpoint = angle

    @property
    def curvature(self) -> float:
        """driving curvature"""
        return math.tan(self.steering_angle) / self.L

    @property
    def wheel_targets(self) -> tuple[float, float]:
        """driving wheel target velocities in m/s"""

        # curvature - left turn is positive, right turn is negative
        cb = self.curvature * self.B / 2  # curvature * half wheel base

        if self.curvature < 0:  # right turn, left wheel is faster
            return (
                self.target_velocity * (1 - cb),
                self.wheels[0].velocity_ms * (1 + cb) / (1 - cb),
            )

        if self.curvature > 0:  # left turn, right wheel is faster
            return (
                self.wheels[1].velocity_ms * (1 - cb) / (1 + cb),
                self.target_velocity * (1 + cb),
            )

        # going straight
        return (self.target_velocity, self.target_velocity)

        # ---- old too simple code ----
        # return (
        #     self.target_velocity * (1 - c * self.B / 2),
        #     self.target_velocity * (1 + c * self.B / 2),
        # )

    @property
    def pose(self) -> Tuple[float, float, float]:
        return (self.xy.x, self.xy.y, self.theta)

    def step(self, dt: float) -> None:
        """update models and internal odometry, motion is governed by the steering wheel, driving wheels may slip"""

        # update steering wheel
        self.steer.step(dt)

        # update driving wheel targets
        for wheel, target in zip(self.wheels, self.wheel_targets):
            wheel.set_velocity_ms(target)
            wheel.step(dt)

        # update position

        # linear distance travelled
        dS = (self.wheels[0].ds + self.wheels[1].ds) / 2

        # update heading
        self.theta += dS * self.curvature

        self.xy += dS * Vector(math.cos(self.theta), math.sin(self.theta))

        # update time
        self.time += dt

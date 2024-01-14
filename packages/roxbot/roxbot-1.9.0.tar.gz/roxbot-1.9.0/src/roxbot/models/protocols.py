#!/usr/bin/env python3
"""
 Interface definition for robot models

 Copyright (c) 2024 ROX Automation - Jev Kuznetsov
"""

from typing import Protocol


class RobotModelProtocol(Protocol):
    """
    Protocol (interface) for a differential drive model class.
    """

    @property
    def velocity(self) -> float:
        """Linear velocity in m/s."""

    @property
    def curvature(self) -> float:
        """Driving curvature."""

    def step(self, dt: float) -> None:
        """
        Perform a timestep.

        Args:
            dt (float): Time delta for the step.
        """

    def cmd_vel(
        self, linear_velocity: float, angular_velocity: float
    ) -> tuple[float, float]:
        """Set wheel velocities from linear and angular velocities.

        Args:
            linear_velocity (float): Linear velocity (v) component.
            angular_velocity (float): Angular velocity (ω) component.
        """

    def cmd_vc(self, linear_velocity: float, curvature: float) -> tuple[float, float]:
        """Set wheel velocities from linear velocity and curvature.

        Args:
            linear_velocity (float): Linear velocity (v) component.
            curvature (float): Curvature (1/R) component.
        """

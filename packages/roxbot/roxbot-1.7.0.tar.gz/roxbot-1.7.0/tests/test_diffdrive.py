""" tests for diff_drive model """

import pytest
from roxbot.models import DiffDriveModel


def test_curvature():
    robot = DiffDriveModel()

    # Test with non-zero velocities
    robot.set_vel(1.0, 2.0)
    robot.step(1.0)
    expected_curvature = 1 / (
        0.5 * robot.DEFAULT_WHEEL_BASE * (1.0 + 2.0) / (2.0 - 1.0)
    )
    assert robot.curvature == pytest.approx(expected_curvature)

    # Test with zero velocity difference
    robot.set_vel(1.0, 1.0)
    robot.step(1.0)
    assert robot.curvature == 0.0


def test_set_pose():
    robot = DiffDriveModel()
    x, y, theta = 1.0, 2.0, 3.1415

    robot.set_pose(x, y, theta)

    assert robot.xy.x == x
    assert robot.xy.y == y
    assert robot.theta == theta


def test_vc_to_vels():
    robot = DiffDriveModel()
    v, c = 1.0, 0.5  # Example values for linear velocity and curvature

    vl, vr = robot.vc_to_vels(v, c)

    # Calculate expected values
    R = 1 / c
    expected_vr = (v * robot.DEFAULT_WHEEL_BASE + 2 * R * v) / 2 / R
    expected_vl = 2 * v - expected_vr

    assert vl == pytest.approx(expected_vl)
    assert vr == pytest.approx(expected_vr)

    # Test with zero curvature
    vl, vr = robot.vc_to_vels(v, 0)
    assert vl == vr == v


def test_repr():
    robot = DiffDriveModel()
    robot.set_vel(1.0, 2.0)

    repr_string = repr(robot)
    expected_string = (
        f"diffdrive vels: ({robot.vl:.2f},{robot.vr:.2f}) C={robot.curvature}"
    )

    assert repr_string == expected_string

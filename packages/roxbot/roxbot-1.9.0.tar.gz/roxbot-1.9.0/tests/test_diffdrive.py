""" tests for diff_drive model """

import pytest
from roxbot.models import DiffDriveModel


@pytest.fixture
def robot():
    # Setup with default or custom parameters
    return DiffDriveModel(wheel_base=0.16, wheel_diameter=0.066, wheel_accel=1e6)


def test_curvature(robot):
    # Test with non-zero velocities
    robot.cmd_lr(1.0, 2.0)
    robot.step(1.0)
    expected_curvature = 1 / (
        0.5 * robot.DEFAULT_WHEEL_BASE * (1.0 + 2.0) / (2.0 - 1.0)
    )
    assert robot.curvature == pytest.approx(expected_curvature)

    # Test with zero velocity difference
    robot.cmd_lr(1.0, 1.0)
    robot.step(1.0)
    assert robot.curvature == 0.0


def test_set_pose(robot):
    x, y, theta = 1.0, 2.0, 3.1415

    robot.pose = (x, y, theta)

    assert robot.xy.x == x
    assert robot.xy.y == y
    assert robot.theta == theta


def test_vc_to_vels(robot):
    v, c = 1.0, 0.5  # Example values for linear velocity and curvature

    vl, vr = robot.cmd_vc(v, c)

    # Calculate expected values
    R = 1 / c
    expected_vr = (v * robot.DEFAULT_WHEEL_BASE + 2 * R * v) / 2 / R
    expected_vl = 2 * v - expected_vr

    assert vl == pytest.approx(expected_vl)
    assert vr == pytest.approx(expected_vr)

    # Test with zero curvature
    vl, vr = robot.cmd_vc(v, 0.0)

    assert vl == vr == v


def test_cmd_vel_straight_line(robot):
    # Test moving in a straight line (angular velocity = 0)
    vl, vr = robot.cmd_vel(1.0, 0.0)  # 1 m/s linear velocity, 0 rad/s angular velocity
    assert vl == 1.0
    assert vr == 1.0


def test_cmd_vel_turn_in_place(robot):
    # Test turning in place (linear velocity = 0)
    vl, vr = robot.cmd_vel(0.0, 1.0)  # 0 m/s linear velocity, 1 rad/s angular velocity
    assert vl == -0.08  # -W/2 * angular_velocity
    assert vr == 0.08  # W/2 * angular_velocity


def test_repr(robot):
    robot.cmd_lr(1.0, 2.0)

    repr_string = repr(robot)
    expected_string = (
        f"diffdrive vels: ({robot.vl:.2f},{robot.vr:.2f}) C={robot.curvature}"
    )

    assert repr_string == expected_string

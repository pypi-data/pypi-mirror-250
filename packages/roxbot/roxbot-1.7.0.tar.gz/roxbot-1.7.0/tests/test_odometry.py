from roxbot.odometry import DiffDriveOdometer
from roxbot.models import DiffDriveModel

from pytest import approx


def test_odometer():
    odo = DiffDriveOdometer(1.0)

    odo.update(1.0, 1.0)

    pose = odo.get_pose()
    assert pose[0] == 1.0
    assert pose[1] == 0.0
    assert pose[2] == 0.0

    odo.set_pose(1.0, 2.0, 3.0)


def test_drive():
    """drive with DiffDriveRobot model and compare results"""

    w = 0.5
    d = 0.2

    robot = DiffDriveModel(wheel_base=w, wheel_diameter=d)
    odo = DiffDriveOdometer(w)

    dt = 0.1

    robot.set_vel(1.0, 0.5)

    for idx in range(100):
        robot.step(dt)
        odo.update(robot.left_wheel.distance, robot.right_wheel.distance)

    robot_pose = robot.pose
    odo_pose = odo.get_pose()

    for idx in range(3):
        assert robot_pose[idx] == approx(odo_pose[idx])

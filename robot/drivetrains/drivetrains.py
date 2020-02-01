from ..motors.motor import Motor

from networktables import NetworkTables

import typing

def _deadzone(value, deadzone):
    """
    Super simple deadzone calculations, just ignore values within the deadzone
    """
    if abs(value) < deadzone:
        return 0
    else:
        return value

class DifferentialDrive:

    l_speed = 0
    r_speed = 0

    # Set default motor type to CIMS unless specified
    motors = [Motor("CIM"), Motor("CIM")]

    # Use the default 10.71/1 gearing from the KOP chassis
    gearing = [0.09337, 0.09337]

    def __init__(self, width, deadzone=0.1):
        self._nt = NetworkTables.getTable("LiveWindow/Ungrouped/DifferentialDrive[1]")
        self.width = width
        self.deadzone = deadzone

    @property
    def left(self):
        return self._nt.getNumber("Left Motor Speed", 0)

    @property
    def right(self):
        return self._nt.getNumber("Right Motor Speed", 0)

    def set_motors(self, left, right):
        self.motors = [left, right]

    def set_gearing(self, left, right):
        self.gearing = [left, right]

    def vector(self, dt) -> typing.Tuple[float, float]:
        l = _deadzone(self.left, self.deadzone) * self.gearing[0] * self.motors[0].free_speed
        r = _deadzone(self.right, self.deadzone) * self.gearing[1] * self.motors[1].free_speed

        forward = (l + r) * 0.5 * dt
        turn = (l - r) / float(self.width) * dt

        self.l_speed = l
        self.r_speed = r
        return forward, turn
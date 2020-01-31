from networktables.util import ntproperty
import toml

motors = toml.load(open('util/motors.toml'))


class Motor:
    def __init__(self, motortype):
        self.motor_type = motortype
        self.free_speed = motors[motortype]["freespeed"]
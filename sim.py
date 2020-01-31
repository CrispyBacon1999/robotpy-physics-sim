import toml
import cv2
import numpy as np
import pint

from robot.robot import Robot
from robot.drivetrains.drivetrains import DifferentialDrive

ureg = pint.UnitRegistry()

config = toml.load(open("physics.toml", 'r'))

ppi = 2
height = config["field"]["height"]
width = config["field"]["width"]
field = np.zeros((width * ppi, height * ppi, 3))

robot_width = config["drivetrain"]["width"]
robot_length = config["drivetrain"]["length"]
robot_rot = config["robot"]["rot"]
robot_x = config["robot"]["x"]
robot_y = config["robot"]["y"]

dt = DifferentialDrive("LiveWindow/Ungrouped/DifferentialDrive[1]", robot_width)
robot = Robot(dt, robot_width, robot_length, position=[robot_x, robot_y], rotation=robot_rot)

while True:
    simfield = np.copy(field)
    pts = np.array(robot.points, np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.fillPoly(simfield, [pts], (0, 255, 255))


    cv2.imshow("Sim", simfield)
    key = cv2.waitKey(5)
    if key != -1:
        print(key)
    if key == 113:
        break
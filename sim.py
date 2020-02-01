import toml
import cv2
import numpy as np

from robot.robot import Robot
from robot.drivetrains.drivetrains import DifferentialDrive
from datetime import datetime

from networktables import NetworkTables

NetworkTables.initialize(server="localhost")

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

drivetrain = DifferentialDrive(robot_width)
robot = Robot(drivetrain, robot_width * ppi, robot_length * ppi, position=[robot_x, robot_y], rotation=robot_rot)
dt = 0
last_time = datetime.now().microsecond / 1000000

while True:
    simfield = np.copy(field)

    robot.update(dt)
    pts = np.array(robot.points, np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.fillPoly(simfield, [pts], (0, 255, 255))

    
    cv2.putText(simfield, f"L: {drivetrain.l_speed:.2f}", (15, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
    cv2.putText(simfield, f"R: {drivetrain.r_speed:.2f}", (15, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
    cv2.putText(simfield, f"F: {robot.forward:.2f}", (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
    cv2.putText(simfield, f"T: {robot.turn:.2f}", (200, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

    cv2.imshow("Sim", simfield)
    key = cv2.waitKey(5)
    if key != -1:
        print(key)
    if key == 113:
        break
    t = datetime.now().microsecond / 1000000
    dt = t - last_time
    last_time = t
    #print(dt)
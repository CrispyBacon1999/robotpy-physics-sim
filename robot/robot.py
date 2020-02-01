import numpy as np


def cart2pol(x, y):
    rho = np.sqrt(x ** 2 + y ** 2)
    phi = np.arctan2(y, x)
    return (rho, phi)


def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return (x, y)

def pol_rotate(rot, rho, phi):
    return (rho, rot + phi)


class Robot:
    def __init__(self, drivetrain, width, length, position=[0, 0], rotation=0):
        self.drivetrain = drivetrain
        self.width = width
        self.length = length
        self.position = position
        self.rotation = rotation
        self.forward = 0
        self.turn = 0
        # Give the polar representation of all the points
        self.basepoints = [
            cart2pol(-self.width / 2.0, self.length / 2.0),
            cart2pol(self.width / 2.0, self.length / 2.0),
            cart2pol(self.width / 2.0, -self.length / 2.0),
            cart2pol(-self.width / 2.0, -self.length / 2.0),
        ]

    def update(self, dt):
        forward, turn = self.drivetrain.vector(dt)
        self.rotation += turn
        turn = np.radians(self.rotation)
        x_com = np.cos(turn)
        y_com = np.sin(turn)
        # rho, phi = cart2pol(*self.position)
        # rho += forward
        # phi += turn

        self.turn = turn
        self.forward = forward
        # self.position = pol2cart(rho, phi)
        self.position[0] += y_com * forward
        self.position[1] += x_com * forward

    @property
    def points(self):
        """
        Gives rotated points of the robot
        FL, FR, RR, RL
        """
        points = np.copy(self.basepoints)

        rot = np.radians(self.rotation)
        # Rotate points (in polar form)
        points = [pol_rotate(rot, *point) for point in points]
        # Convert back to cartesian
        points = [pol2cart(*point) for point in points]
        # Add the positional offset
        points = [(x + self.position[0], y + self.position[1]) for x,y in points]
        return points




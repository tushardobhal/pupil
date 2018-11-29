import numpy as np
from numpy.linalg import inv
import filterpy.kalman

def tracker_4dof(noise=0.02, time=1.0):
    q = noise
    dt = time
    tracker = filterpy.kalman.KalmanFilter(dim_x=8, dim_z=2)
    tracker.x = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    tracker.F = np.array([[1., 0., dt, 0., 1 / 2 * (dt ** 2), 0., 1 / 6 * (dt ** 3), 0],
                          [0., 1., 0., dt, 0., 1 / 2 * (dt ** 2), 0., 1 / 6 * (dt ** 3)],
                          [0., 0., 1., 0., dt, 0., 1 / 2 * (dt ** 2), 0],
                          [0., 0., 0., 1., 0, dt, 0., 1 / 2 * (dt ** 2)],
                          [0., 0., 0., 0., 1., 0., dt, 0.],
                          [0., 0., 0., 0., 0, 1., 0., dt],
                          [0., 0., 0., 0., 0, 0., 1., 0.],
                          [0., 0., 0., 0., 0, 0., 0., 1.]])
    tracker.H = np.array([[1., 0., 0., 0., 0., 0., 0., 0.],
                          [0., 1., 0., 0., 0., 0., 0., 0.],])
    tracker.R = np.array([[1.0, 0],
                          [0, 1.0]])
    tracker.P = np.eye(8) * 1000.
    tracker.Q = np.array([[0., 0., q, 0., q, 0., q, 0.],
                          [0., 0., 0., q, 0., q, 0., q],
                          [q, 0., q, 0., q, 0., q, 0.],
                          [0., q, 0., q, 0., q, 0., q],
                          [q, 0., q, 0., q, 0., q, 0.],
                          [0., q, 0., q, 0., q, 0., q],
                          [q, 0., q, 0., q, 0., q, 0.],
                          [0., q, 0., q, 0., q, 0., q]])
    return tracker


class OnlineKalman:

    def __init__(self, kalman_filter, current_state, max_vel=50):
        """
        kalman_filter: type of kalman filter to use

        """
        self.prev_state = np.array([current_state[0], current_state[1]])
        self.cur_time = current_state[2]
        self.eps_max = 0.6
        self.scale = 10
        self.dumb = 0
        self.kalman = kalman_filter

        self.max_vel = max_vel

        self.old_Q = self.kalman.Q
        self.kalman.predict()
        self.kalman.update(self.prev_state)
        self.cur_state = (self.kalman.x[0], self.kalman.x[1])

        res = self.kalman.y
        eps = np.dot(res.T, inv(self.kalman.S)).dot(res)
        if eps > self.eps_max:
            self.kalman.Q = self.old_Q*self.scale
            self.dumb += 1
        elif self.dumb > 0:
            self.kalman.Q = self.old_Q
            self.dumb -= 1

    @staticmethod
    def distance(c1, c2):
        return np.sqrt((c2[0]-c1[0]) ** 2 + (c2[1]-c1[1]) ** 2)

    def reject_state(self, new_state):
        """
        new_state: (x,y,t)
        """
        pt1 = self.cur_state
        t1 = self.cur_time

        pt2 = (round(new_state[0], 4),round(new_state[1], 4))
        t2 = new_state[2]

        new_vel = distance(pt1, pt2) / (t2-t1)

        if new_vel > self.max_vel:
            return True
        else:
            return False

    def predict(self, new_state):
        """
        new_state: (x,y,t)
        """
        if self.reject_state(new_state):
            self.prev_state = self.cur_state
        else:
            self.prev_state = (new_state[0], new_state[1])

        self.cur_time = new_state[2]

        self.kalman.predict()
        self.kalman.update(self.prev_state)
        self.cur_state = (self.kalman.x[0], self.kalman.x[1])

        res = self.kalman.y
        eps = np.dot(res.T, inv(self.kalman.S)).dot(res)
        if eps > self.eps_max:
            self.kalman.Q = self.old_Q*self.scale
            self.dumb += 1
        elif self.dumb > 0:
            self.kalman.Q = self.old_Q
            self.dumb -= 1

        return (self.kalman.x[0], self.kalman.x[1], self.cur_time)


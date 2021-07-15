from .DatatypeHandler import DatatypeHandler
import numpy as np

def eulerToQuaternion(roll, pitch, yaw):
        print("Roll={0}\nPitch={1}\nYaw={2}".format(roll, pitch, yaw))
        cr = np.cos(roll * 0.5)
        sr = np.sin(roll * 0.5)
        cp = np.cos(pitch * 0.5)
        sp = np.sin(pitch * 0.5)
        cy = np.cos(yaw *  0.5)
        sy = np.sin(yaw * 0.5)

        # https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
        w = cr * cp * cy + sr * sp * sy
        x = sr * cp * cy - cr * sp * sy
        y = cr * sp * cy + sr * cp * sy
        z = cr * cp * sy - sr * sp * cy

        return np.array([w,x,y,z])

class EulerAngleHandler(DatatypeHandler):
    def get_quaternions(self, data, start_column, time_column):
        RADIANS_PER_DEGREE = (2 * np.pi) / 360.0
        """
        Overriddes parent method. 
        Assumes input data is in the form of Euler angles in degrees.
        """
        quaternion_list = []
        for line in data:
            if len(line) <= start_column + 2 or line[0] == '#':
                continue
            roll = float(line[start_column]) * RADIANS_PER_DEGREE
            pitch = float(line[start_column+1]) * RADIANS_PER_DEGREE
            yaw = float(line[start_column+2]) * RADIANS_PER_DEGREE
            quaternion_list.append(eulerToQuaternion(roll, pitch, yaw))
        return quaternion_list

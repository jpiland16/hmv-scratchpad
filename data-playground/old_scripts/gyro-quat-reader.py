import numpy as np
# class DirectQuatReader(QuatReader):
#     def __init__(self, filepath, col_offset):
#         self.filepath = filepath


#     def get_quaternions(self):
#         """Reads the quaternions directly from the file"""
#         pass 

def ham_product(q1, q2):
    """ Returns Hamilton product q1q2 for two quaternions
    https://en.wikipedia.org/wiki/Quaternion#Hamilton_product
    """
    prod = np.empty(4)
    prod[0] = q1[0]*q2[0] - q1[1]*q2[1] - q1[2]*q2[2] - q1[3]*q2[3]
    prod[1] = q1[0]*q2[1] + q1[1]*q2[0] + q1[2]*q2[3] - q1[3]*q2[2]
    prod[2] = q1[0]*q2[2] - q1[1]*q2[3] + q1[2]*q2[0] + q1[3]*q2[1]
    prod[3] = q1[0]*q2[3] + q1[1]*q2[2] - q1[2]*q2[1] + q1[3]*q2[0]
    return prod


def madgwick_estimate(q_curr, gyro_data, elapsed_time):
    """Implements the technique in the Madgwick paper using only gyro data.
    The only difference between this and the graph-gyro-data.py implementation 
    is that we put all the gyro data into one quaternion instead of composing
    rotations.
    params:
        q_curr: current orientation quaternion in w,x,y,z form
        gyro_data: gyro data in x,y,z radians
        elapsed_time: time between readings in seconds
    """
    q_gyro = np.zeros(4)
    q_gyro[1:4] = gyro_data
    q_dot = ham_product(q_curr, q_gyro)
    q_new = q_dot * elapsed_time
    return q_new / np.linalg.norm(q_new)



if __name__=='__main__':
    print("hello world")
import numpy as np

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


def vec_quat_mult(vec, quat):
    """ Multiplies vector3 vec by unit quaternion quat and returns the 
    resulting rotated vector
    """
    vec_extended = np.concatenate((0, vec), axis=None)
    quat_inverse = np.array([quat[0], -quat[1], -quat[2], -quat[3]])
    final_prod = ham_product(ham_product(quat, vec_extended), quat_inverse)
    return final_prod[1:4]

if __name__=='__main__':    
    q1 = np.array([0.707, 0, 0, 0.707]) #rotation of 90 degrees CCW about the x-axis
    q2 = np.array([0, 0, 0.707, 0.707]) #rotation of 90 degrees CCW about the z-axis
    q3 = np.array([0.707, 0, 0, -0.707]) #rotation of 270 degrees CCW about the x-axis
    print("Sophie intermediate product: {0}".format(ham_product(q2,q1)))
    print("Sophie product: {0}".format(ham_product(q3, ham_product(q2, q1))))
    sensor_heading_local = np.array([1,0,0])
    quat_data = np.array([0.6779879364607869, 0.6214175397860577, 0.2008291762011785, 0.3374021950821352])
    sensor_heading_opp = vec_quat_mult(sensor_heading_local, quat_data)
    quat_t_o = np.array([1/2, -1/2, -1/2, -1/2])
    sensor_heading_three = vec_quat_mult(sensor_heading_opp, quat_t_o)
    quat_sensor_o = ham_product(quat_t_o, quat_data)
    sensor_heading_composite = vec_quat_mult(sensor_heading_local, quat_sensor_o)
    print("Transformation from sensor to opporunity space: {0}".format(quat_data))
    print("Transformation from opportunity to three space: {0}".format(quat_t_o))
    print("Transformation from sensor to three space: {0}".format(quat_sensor_o))
    print("Direction of sensor in sensor space: {0}".format(sensor_heading_local))
    print("Direction of sensor in opportunity space: {0}".format(sensor_heading_opp))
    print("Direction of sensor in three space: {0}".format(sensor_heading_three))
    print("Direction of sensor in three space using composite quaternion: {0}".format(sensor_heading_composite))
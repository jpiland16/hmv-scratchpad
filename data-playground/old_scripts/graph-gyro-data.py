from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import argparse


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


def quat_from_axis_angle(axis, angle):
    """Angle should be in radians CCW
    """
    quat = np.empty(4)
    quat[0] = np.cos(angle/2)
    quat[1:4] = np.sin(angle/2) * axis
    return quat / np.linalg.norm(quat)


def update_sensor(frame_num, heading_data, axes_plot):
    axes_plot.set_data(heading_data[0:2, :frame_num+1])
    axes_plot.set_3d_properties(heading_data[2, :frame_num+1])
    return axes_plot


def quaternions_from_gyro(filename, verbose, line_offset, max_lines):
    quat_list = []
    prev_transf = np.array([1,0,0,0])
    basis_vecs = np.array([[1.,0,0],[0,1.,0],[0,0,1.]]) # These have to be explicity declared as floats
    with open(filename) as f:
        lines = f.readlines()[0:max_lines]
        print("Number of lines read: {0}".format(len(lines)))
        for line in lines:
            data_points = line.split(' ')
            if data_points[0] == "#":
                continue
            first_col = line_offset if line_offset else 0
            # Why multiply by a factor of 33/10^6? 
            # We divide by 1000 because the data is all multiplied by 1000 to convert floats to ints
            # Then we multiply by 33/1000 because the units are radians/sec and 33/1000 seconds have passed.
            gyro_vals = [float(data_points[first_col+i]) * (33.0 / 1000.0**2) for i in range(3)]
            if verbose:
                print("gyro vals: ", gyro_vals)

            # The first thing to notice is that all rotation is ~double-counted.
            # For example, moving perpendicular to the x-axis is rotation around
            # the z-axis and around the y-axis.
            quats = [quat_from_axis_angle(basis_vecs[i], 0.5 * gyro_vals[i]) for i in range(3)]
            curr_transf = ham_product(ham_product(quats[0], quats[1]), quats[2])
            
            curr_transf = ham_product(curr_transf, prev_transf)
            prev_transf = curr_transf
            quat_list.append(curr_transf)
    return quat_list


def madgwick_estimate(q_curr, gyro_data, elapsed_time):
    """Implements the technique in the Madgwick paper using only gyro data.
    The only difference between this and the graph-gyro-data.py implementation 
    is that we put all the gyro data into one quaternion instead of composing
    rotations.
    params:
        q_curr: current orientation quaternion in w,x,y,z form
        gyro_data: gyro data in x,y,z radians/second
        elapsed_time: time between readings in seconds
    """
    q_gyro = np.zeros(4)
    q_gyro[1:4] = gyro_data
    q_dot = ham_product(q_curr, q_gyro) * 0.5
    q_new = q_curr + (q_dot * elapsed_time)
    return q_new / np.linalg.norm(q_new)


def madgwick_quat_from_gyro(filename, verbose, line_offset, max_lines):
    quat_list = []
    prev_transf = np.array([1,0,0,0])
    basis_vecs = np.array([[1.,0,0],[0,1.,0],[0,0,1.]]) # These have to be explicity declared as floats
    with open(filename) as f:
        lines = f.readlines()[0:max_lines]
        print("Number of lines read: {0}".format(len(lines)))
        for line in lines:
            data_points = line.split(' ')
            if data_points[0] == "#":
                continue
            first_col = line_offset if line_offset else 0
            # All values from the data are divided by 1000.0 because they were
            # multiplied by 1000 to convert from int to float.
            gyro_vals = [float(data_points[first_col+i]) * (1 / 1000.0) for i in range(3)]
            gyro_vals = np.array(gyro_vals)

            curr_transf = madgwick_estimate(prev_transf, gyro_vals, 33.0/1000)
            
            prev_transf = curr_transf
            quat_list.append(curr_transf)
    return quat_list



if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Filepath of the data to use")
    parser.add_argument("--offset", "--o", help="Number of columns into the data file to start reading", type=int)
    parser.add_argument("--maxlines", "--max", help="Max number of rows to read from  file", type=int)
    parser.add_argument("--verbose", "--v", help="Use to enable print statements", action="store_true")
    args = parser.parse_args()

    x_vec = np.array([1,0,0])
    z_vec = np.array([0,0,1])

    # It is not clear whether the gyro data is in degrees or radians so I am going to
    # check by reading the values.
    # Update: Since we rotate at a rate of no more than 1.15 units / sec, 
    # it's probably radians.

    # quat_list = []
    # prev_transf = np.array([1,0,0,0])
    # basis_vecs = np.array([[1.,0,0],[0,1.,0],[0,0,1.]]) # These have to be explicity declared as floats
    # with open(args.file) as f:
    #     lines = f.readlines()[0:args.maxlines]
    #     print("Number of lines read: {0}".format(len(lines)))
    #     for line in lines:
    #         data_points = line.split(' ')
    #         if data_points[0] == "#":
    #             continue
    #         first_col = args.offset if args.offset else 0
    #         # Why multiply by a factor of 33/10^6? 
    #         # We divide by 1000 because the data is all multiplied by 1000 to convert floats to ints
    #         # Then we multiply by 33/1000 because the units are radians/sec and 33/1000 seconds have passed.
    #         gyro_vals = [float(data_points[first_col+i]) * (33.0 / 1000.0**2) for i in range(3)]
    #         if args.verbose:
    #             print("gyro vals: ", gyro_vals)

    #         # The first thing to notice is that all rotation is ~double-counted.
    #         # For example, moving perpendicular to the x-axis is rotation around
    #         # the z-axis and around the y-axis.
    #         quats = [quat_from_axis_angle(basis_vecs[i], 0.5 * gyro_vals[i]) for i in range(3)]
    #         curr_transf = ham_product(ham_product(quats[0], quats[1]), quats[2])
            
    #         curr_transf = ham_product(curr_transf, prev_transf)
    #         prev_transf = curr_transf
    #         quat_list.append(curr_transf)
    data_quats = madgwick_quat_from_gyro(args.file, args.verbose, args.offset, args.maxlines)

    x_vec = np.array([1,0,0])
    x_orientations = []
    for quat in data_quats:
            x_curr = vec_quat_mult(x_vec, quat)
            x_orientations.append(x_curr)
        
    x_pts = np.array(x_orientations).T
    if args.verbose:
        print("x_pts:", x_pts)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    pos_plot = ax.plot(x_pts[0], x_pts[1], x_pts[2], label='Position of sensor')[0]
    # plt.plot(times, angles)
    # plt.show()

    millisecond_interval = 33
    line_ani = animation.FuncAnimation(fig, update_sensor, frames=len(x_pts[0]), fargs=(x_pts, pos_plot), interval=millisecond_interval)
    plt.show()
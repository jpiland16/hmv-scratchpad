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

    x_orientations = []

    curr_x = np.array([1,0,0])
    curr_y = np.array([0,1,0])
    curr_z = np.array([0,0,1])
    basis_vecs = np.array([[1.,0,0],[0,1.,0],[0,0,1.]]) # These have to be explicity declared as floats
    with open(args.file) as f:
        lines = f.readlines()[0:args.maxlines]
        print("Number of lines read: {0}".format(len(lines)))
        for line in lines:
            data_points = line.split(' ')
            if data_points[0] == "#":
                continue
            first_col = args.offset if args.offset else 0
            # Why multiply by a factor of 33/10^6? 
            # We divide by 1000 because the data is all multiplied by 1000 to convert floats to ints
            # Then we multiply by 33/1000 because the units are radians/sec and 33/1000 seconds have passed.
            gyro_vals = [float(data_points[first_col+i]) * (33.0 / 1000.0**2) for i in range(3)]
            if args.verbose:
                print("gyro vals: ", gyro_vals)

            # The first thing to notice is that all rotation is ~double-counted.
            # For example, moving perpendicular to the x-axis is rotation around
            # the z-axis and around the y-axis.
            quats = [quat_from_axis_angle(basis_vecs[i], 0.5 * gyro_vals[i]) for i in range(3)]
            curr_transf = ham_product(ham_product(quats[0], quats[1]), quats[2])
            if args.verbose:
                print("basis vectors before change: ", basis_vecs)
            for i in range(len(basis_vecs)):
                basis_vecs[i] = vec_quat_mult(basis_vecs[i], curr_transf)
            if args.verbose:
                print("basis vectors after change: ", basis_vecs)
            x_orientations.append(basis_vecs[0].copy())

            if args.verbose:
                print("Gyro: rotation around axes = {0}".format(gyro_vals))
        
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
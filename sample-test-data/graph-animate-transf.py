from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import sys


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
    print("original quat: {0}".format(quat))
    vec_extended = np.concatenate((0, vec), axis=None)
    print("extended vector: {0}".format(vec_extended))
    quat_inverse = np.array([quat[0], -quat[1], -quat[2], -quat[3]])
    print("inverse quat: {0}".format(quat_inverse))
    final_prod = ham_product(ham_product(quat, vec_extended), quat_inverse)
    return final_prod[1:4]

# https://matplotlib.org/stable/gallery/animation/random_walk.html#sphx-glr-gallery-animation-random-walk-py
def update_sensor(frame_num, heading_data, axes_plot):
    axes_plot.set_data(heading_data[0:2, :frame_num])
    axes_plot.set_3d_properties(heading_data[2, :frame_num])
    return axes_plot


def update_arrow(frame_num, location_data, heading_data, quivers):
    fd_location = [location_data[0][frame_num],location_data[1][frame_num],location_data[2][frame_num]]
    fd_endpoint = [location_data[0][frame_num]*2,location_data[1][frame_num]*2,location_data[2][frame_num]*2]

    new_location = [location_data[0][frame_num],location_data[1][frame_num],location_data[2][frame_num]]
    new_endpoint = [heading_data[0][frame_num],heading_data[1][frame_num],heading_data[2][frame_num]]
    for i in range(3):
        new_endpoint[i] = new_endpoint[i] + new_location[i]


    new_up_segs = [[new_location, new_endpoint]]
    quivers[0].set_segments(new_up_segs)
    
    new_fd_segs = [[fd_location, fd_endpoint]]
    quivers[1].set_segments(new_fd_segs)
    # quiv.set_segments(heading_data[0][frame_num], heading_data[1][frame_num], heading_data[2][frame_num])
    return quivers


if __name__=='__main__':

    x_vec = np.array([1,0,0])
    z_vec = np.array([0,0,1])

    # graph result
    pointervals = []
    shouldervals = []
    with open(sys.argv[1]) as f:
        for line in f:
            data_points = line.split(' ')
            if data_points[0] == "#":
                continue
            curr_quat = np.empty(4)
            # read quaternion from line
            for i in range(4):
                curr_quat[i] = float(data_points[i])
            x_new = vec_quat_mult(x_vec, curr_quat)
            print("{0} mult by {1}:".format(x_vec, curr_quat))
            print(x_new)
            print("")
            pointervals.append(x_new)
            z_new = vec_quat_mult(z_vec, curr_quat)
            shouldervals.append(z_new)
    pointervals = np.array(pointervals).T
    shouldervals = np.array(shouldervals).T
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    # I need a better name than 'position of sensor' and a better way to show it.
    # What I'm actually showing is the vector representing local sensor x (forward).
    sensor_path = ax.plot(pointervals[0], pointervals[1], pointervals[2], label='Position of sensor')[0]
    up_quiver = ax.quiver(pointervals[0], pointervals[1], pointervals[2], shouldervals[0], shouldervals[1], shouldervals[2], edgecolors="orange", length=0.45, label='Local sensor up (z)')
    fd_quiver = ax.quiver(pointervals[0], pointervals[1], pointervals[2], shouldervals[0], shouldervals[1], shouldervals[2], edgecolors="green", length=0.45, label='Local sensor forward (x)')
    ax.set_xlim((-1.1, 1.1))
    ax.set_xlabel('x')
    ax.set_ylim((-1.1, 1.1))
    ax.set_ylabel('y')
    ax.set_zlim((-1.1, 1.1))
    ax.set_zlabel('z')
    ax.legend()

    line_ani = animation.FuncAnimation(fig, update_sensor, 30, fargs=(pointervals, sensor_path), interval=50)
    quiv_ani = animation.FuncAnimation(fig, update_arrow, 30, fargs=(pointervals, shouldervals, [up_quiver, fd_quiver]), interval=50)
    plt.show()
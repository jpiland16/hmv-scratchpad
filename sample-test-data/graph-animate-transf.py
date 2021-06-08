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

# https://matplotlib.org/stable/gallery/animation/random_walk.html#sphx-glr-gallery-animation-random-walk-py
def update_sensor(frame_num, heading_data, axes_plot):
    axes_plot.set_data(heading_data[0:2, :frame_num+1])
    axes_plot.set_3d_properties(heading_data[2, :frame_num+1])
    return axes_plot


def update_arrow(frame_num, location_data, heading_data, right_data, quivers):
    fd_location = [location_data[0][frame_num],location_data[1][frame_num],location_data[2][frame_num]]
    fd_endpoint = [location_data[0][frame_num],location_data[1][frame_num],location_data[2][frame_num]]
    for i in range(3):
        fd_endpoint[i] = fd_location[i] + fd_endpoint[i]    
    new_fd_segs = [[fd_location, fd_endpoint]]
    quivers[1].set_segments(new_fd_segs)

    up_endpoint = [heading_data[0][frame_num],heading_data[1][frame_num],heading_data[2][frame_num]]
    for i in range(3):
        up_endpoint[i] = fd_location[i] + up_endpoint[i]
    new_up_segs = [[fd_location, up_endpoint]]
    quivers[0].set_segments(new_up_segs)

    right_endpoint = [right_data[0][frame_num],right_data[1][frame_num],right_data[2][frame_num]]
    for i in range(3):
        right_endpoint[i] = fd_location[i] + right_endpoint[i]
    new_right_segs = [[fd_location, right_endpoint]]
    quivers[2].set_segments(new_right_segs)
    
    # quiv.set_segments(heading_data[0][frame_num], heading_data[1][frame_num], heading_data[2][frame_num])
    return quivers


if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Filepath of the data to use")
    parser.add_argument("--offset", "--o", help="Number of columns into the data file to start reading", type=int)
    parser.add_argument("--float", help="Divide input values by 1000", action="store_true")
    parser.add_argument("--maxlines", "--max", help="Max number of rows to read from  file", type=int)
    args = parser.parse_args()

    x_vec = np.array([1,0,0])
    y_vec = np.array([0,1,0])
    z_vec = np.array([0,0,1])

    # I really need to implement flags for this
    start_column = args.offset if args.offset else 0
    max_lines = args.maxlines if args.maxlines else -1
    line_skipping = 1 # Only read the first line for each block of line_skipping lines.
    # if len(sys.argv) > 5:
    #     line_skipping = int(sys.argv[5])

    # graph result
    pointervals = []
    shouldervals = []
    rightvals = []
    line_num = 0
    with open(args.file) as f:
        for line in f:
            line_num += 1
            if max_lines != -1 and line_num > max_lines:
                break
            data_points = line.split(' ')
            if data_points[0] == "#":
                continue
            curr_quat = np.empty(4)
            # read quaternion from line
            for i in range(4):
                data_pt = float(data_points[i+start_column])
                curr_quat[i] = data_pt / 1000.0 if args.float else data_pt
            x_new = vec_quat_mult(x_vec, curr_quat)
            # print("{0} mult by {1}:".format(x_vec, curr_quat))
            # print(x_new)
            # print("")
            pointervals.append(x_new)
            z_new = vec_quat_mult(z_vec, curr_quat)
            shouldervals.append(z_new)
            y_new = vec_quat_mult(y_vec, curr_quat)
            rightvals.append(y_new)
    pointervals = np.array(pointervals).T
    shouldervals = np.array(shouldervals).T
    rightvals = np.array(rightvals).T
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    # I need a better name than 'position of sensor' and a better way to show it.
    # What I'm actually showing is the vector representing local sensor x (forward).
    sensor_path = ax.plot(pointervals[0], pointervals[1], pointervals[2], label='Position of sensor')[0]
    up_quiver = ax.quiver(pointervals[0], pointervals[1], pointervals[2], shouldervals[0], shouldervals[1], shouldervals[2], edgecolors="orange", length=0.45, label='Local sensor up (z)')
    fd_quiver = ax.quiver(pointervals[0], pointervals[1], pointervals[2], shouldervals[0], shouldervals[1], shouldervals[2], edgecolors="green", length=0.45, label='Local sensor forward (x)')
    right_quiver =  ax.quiver(pointervals[0], pointervals[1], pointervals[2], shouldervals[0], shouldervals[1], shouldervals[2], edgecolors="blue", length=0.45, label='Local sensor left (y)')
    
    ax.set_xlim((-1.1, 1.1))
    ax.set_xlabel('x (North-South)')
    ax.set_ylim((-1.1, 1.1))
    ax.set_ylabel('y (East-West)')
    ax.set_zlim((-1.1, 1.1))
    ax.set_zlabel('z (Up-Down)')
    ax.legend()

    millisecond_interval = 33 * line_skipping
    line_ani = animation.FuncAnimation(fig, update_sensor, frames=len(pointervals[0]), fargs=(pointervals, sensor_path), interval=millisecond_interval)
    quiv_ani = animation.FuncAnimation(fig, update_arrow, frames=len(pointervals[0]), fargs=(pointervals, shouldervals, rightvals, [up_quiver, fd_quiver, right_quiver]), interval=millisecond_interval)
    plt.show()
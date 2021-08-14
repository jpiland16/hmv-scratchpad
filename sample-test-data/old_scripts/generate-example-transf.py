"""Generates data representing orientation of a joint as it moves in an outward-facing 
	cone pattern (like if you're rotating your shoulder).
Let the XSens device point North=(1,0,0), then apply the quaternion as a transformation
	and you have where the XSens device is actually pointing in global coordinates.
Has the format (C,XS,YS,ZS) where C=cos(theta) and S=sin(theta),
	since that's a standard way to represent orientation quaternions.
"""

import numpy as np
import sys


def generate_points(t_r, t_max, t_step, v_up, v_forward, v_out):
	t = 0
	vectors = []
	while (t < t_max):
		angle = (2*np.pi/t_r) * t
		rot_axis = v_out + np.cos(angle)*v_forward + np.sin(angle)*v_up
		rot_axis = rot_axis / np.linalg.norm(rot_axis)
		vectors.append(rot_axis)
		t += t_step
	return vectors


def quat_multiply(q1, q2):
	w1 = q1[0]
	v1 = q1[1:4]
	w2 = q2[0]
	v2 = q2[1:4]

	q_prod = np.empty(4)
	q_prod[0] = w1*w2 - np.dot(v1,v2)
	q_prod[1:4] = w1*v2 + w2*v1 + np.cross(v1, v2)
	return q_prod


def quat_from_axis_angle(axis, angle):
	quat = np.empty(4)
	quat[0] = np.cos(angle/2)
	quat[1:4] = np.sin(angle/2)*axis
	return quat


# Problem: There are a family of quaternions that represent pointing a unit
# vector in a specified direction, since we have a free variable. How do we
# deal with the z and y axes?
def quat_from_vec(start_vec, end_vec):
	cross_prod = np.cross(start_vec, end_vec)
	dot_prod = np.dot(start_vec, end_vec)
	w = np.sqrt(np.linalg.norm(start_vec)**2 + np.linalg.norm(end_vec)**2) + dot_prod
	return np.concatenate((cross_prod, w), axis=None)


def sphere_coord_point(sphere_theta, sphere_phi):
	coord_point = np.empty(3)
	coord_point[0] = np.cos(sphere_theta)*np.sin(sphere_phi)
	coord_point[1] = np.sin(sphere_theta)*np.sin(sphere_phi)
	coord_point[2] = np.cos(sphere_phi)
	return coord_point


# https://en.wikipedia.org/wiki/Rotation_matrix#Quaternion
def quat_from_matrix(rot_mat):
	quat = np.empty(4)
	t = rot_mat[0][0] + rot_mat[1][1] + rot_mat[2][2]
	r = np.sqrt(1+t)
	s = 1/(2*r)
	quat[0] = r/2
	quat[1] = (rot_mat[2][1] - rot_mat[1][2])*s
	quat[2] = (rot_mat[0][2] - rot_mat[2][0])*s
	quat[3] = (rot_mat[1][0] - rot_mat[0][1])*s
	return quat


def generate_data_new():
	"""
	These quaternions represent the arm tracing out a circle on the
		xz plane, where x is north-south and z is up-down,
		while the arm is also pointing in the positive y (east) direction.
		The palm is pointing tangent to the circle.
		They should be printed in w,x,y,z format.
	"""
	t_final = 1.0
	t_step = 1.0/30.0
	t_curr = 0

	# forward = north = x
	# out = east = y
	# up = up = z

	generated_quats = []

	while (t_curr < t_final):
		theta = 2*np.pi*t_curr
		arm_direction = np.array([np.cos(theta), 1.0, np.sin(theta)])  # new x after transformation
		tangent_direction = np.array([-np.sin(theta), 0.0, np.cos(theta)])
		out_direction = np.cross(arm_direction, tangent_direction) #new y after tansform

		#Switch between this code and the below code block
		# orientation_quat = np.empty(4)
		# orientation_quat[0] = 1 + np.dot(np.array([1,0,0]), arm_direction)
		# orientation_quat[1:4] = np.cross(np.array([1,0,0]), arm_direction)
		# orientation_quat = orientation_quat / np.linalg.norm(orientation_quat)

		rotation_mat = np.empty([3,3])
		rotation_mat[0:3][0] = arm_direction / np.linalg.norm(arm_direction)
		rotation_mat[0:3][1] = tangent_direction / np.linalg.norm(tangent_direction)
		rotation_mat[0:3][2] = out_direction / np.linalg.norm(out_direction)
		orientation_quat = quat_from_matrix(rotation_mat)

		generated_quats.append(orientation_quat)
		t_curr += t_step
	return generated_quats


def create_printed_data(output_filepath):
	data_quats = generate_data_new()
	with open(output_filepath, 'w') as f:
		for quat in data_quats:
			print('{0} {1} {2} {3}'.format(quat[0], quat[1], quat[2], quat[3]), file=f)
		f.close()	


def generate_data(output_filepath, num_columns, column_index):
	up = np.array([0.0, 1.0, 0.0])
	forward = np.array([0.0, 0.0, 1.0])
	out = np.array([-1.0, 0.0, 0.0])
	north = np.array([1.0, 0.0, 0.0])

	data_vecs = generate_points(1.0, 1.0, 1.0/30, up, forward, out)
	output_vecs = []
	for vec in data_vecs:
		output_vecs.append(quat_from_vec(north, vec))
	right_padding = num_columns - column_index - 4
	with open(output_filepath, 'w') as f:
		for vec in output_vecs:
			for i in range(column_index):
				print('0 ', end='', file=f)
			print('{0} {1} {2} {3} '.format(vec[0], vec[1], vec[2], vec[3]), end='', file=f)
			for i in range(right_padding-1):
				print('0 ', end='', file=f)
			print('0', file=f)
		f.close()



if __name__=='__main__':
	# if len(sys.argv) < 2 or len(sys.argv) > 4 or sys.argv[1] == 'usage':
	# 	print('usage: python generate-example-data.py <output-path> [optional:#columns] [optional:column-offset]')
	# 	sys.exit(0)
	# num_col = 5
	# col_offset = 0
	# if (len(sys.argv) > 2):
	# 	num_col = int(sys.argv[2])
	# if (len(sys.argv) > 3):
	# 	col_offset = int(sys.argv[3])
	# generate_data(sys.argv[1], num_col, col_offset)
	create_printed_data("transf-output-20210526.txt")
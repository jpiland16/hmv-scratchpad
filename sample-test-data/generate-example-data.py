"""Generates data representing orientation of a join as it moves in an outward-facing 
	cone pattern (like if you're rotating your shoulder).
Outputs this data as (x, y, z, theta), where (x,y,z) are the axis that the bone is 
	pointing and theta is how much the bone is twisted about the axis.
May be changed to have the format (C,XS,YS,ZS) where C=cos(theta) and S=sin(theta),
	since that's a standard way to represent orientation quaternions.
"""

import numpy as np
import sys


def generate_points(t_r, t_max, t_step, v_up, v_forward, v_out):
	t = 0
	vectors = []
	while (t < t_max):
		twist_angle = 0
		angle = (2*np.pi/t_r) * t
		rot_axis = v_out + np.cos(angle)*v_forward + np.sin(angle)*v_up
		rot_axis = rot_axis / np.linalg.norm(rot_axis)
		rot_axis = np.concatenate((rot_axis , 0), axis=None)
		vectors.append(rot_axis)
		t += t_step
	return vectors


def generate_data(output_filepath, num_columns, column_index):
	up = np.array([0.0, 1.0, 0.0])
	forward = np.array([1.0, 0.0, 0.0])
	out = np.array([0.0, 0.0, 1.0])

	data_vecs = generate_points(1.0, 1.0, 1.0/30, up, forward, out)
	right_padding = num_columns - column_index - 4
	with open(output_filepath, 'w') as f:
		for vec in data_vecs:
			for i in range(column_index):
				print('0 ', end='', file=f)
			print('{0} {1} {2} {3} '.format(vec[0], vec[1], vec[2], vec[3]), end='', file=f)
			for i in range(right_padding-1):
				print('0 ', end='', file=f)
			print('0', end='', file=f)
			print("", file=f)
		f.close()


if __name__=='__main__':
	if len(sys.argv) < 2 or len(sys.argv) > 4 or sys.argv[1] == 'usage':
		print('usage: python generate-example-data.py <output-path> [optional:#columns] [optional:column-offset]')
		sys.exit(0)
	num_col = 5
	col_offset = 0
	if (len(sys.argv) > 2):
		num_col = int(sys.argv[2])
	if (len(sys.argv) > 3):
		col_offset = int(sys.argv[3])
	generate_data(sys.argv[1], num_col, col_offset)
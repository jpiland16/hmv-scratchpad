import ctypes
import ctypes.util
import os
import numpy as np

from .DatatypeHandler import DatatypeHandler

RADIANS_PER_DEGREE = (np.pi * 2) / 360
DEGREES_PER_RADIAN = 1 / RADIANS_PER_DEGREE

def eulerToQuaternion(roll, pitch, yaw):
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

class AGMAltHandler(DatatypeHandler):
    def get_quaternions(self, data, start_column, time_column):
        SAMPLE_RATE = 25.0 # Hz
        float_type = ctypes.c_float
        float_pointer_type = ctypes.POINTER(float_type)

        create_float_array = float_type * 9
        create_float_array_array = float_pointer_type * len(data)

        data_ptr = create_float_array_array()
        for i in range(len(data)):
            data_ptr[i] = create_float_array()
            for j in range(0, 3):
                data_ptr[i][j] = data[i][j+start_column]
            for j in range(3, 6):
                data_ptr[i][j] = data[i][j+start_column] * DEGREES_PER_RADIAN
            for j in range(6, 9):
                data_ptr[i][j] = data[i][j+start_column]

        create_output_array = float_type * 3
        create_output_2d_array = float_pointer_type * len(data)        

        output_ptr = create_output_2d_array()
        for i in range(len(data)):
            output_ptr[i] = create_output_array()

        # Source of Fusion Library:
        # https://github.com/xioTechnologies/Fusion
        # Authors: x-io Technologies, Riccardo Miccini
        # License: GNU general public license
        libname = os.path.dirname(__file__)+'/build/FuseDataArray.so'
        c_lib = ctypes.CDLL(libname)
        c_lib.eulerFromDoubles(data_ptr, ctypes.c_int(len(data)), output_ptr, ctypes.c_float(1.0/SAMPLE_RATE))
        quaternion_list = []
        for i in range(len(data)):
            quat_orientation = eulerToQuaternion(output_ptr[i][0] * RADIANS_PER_DEGREE, output_ptr[i][1] * RADIANS_PER_DEGREE, output_ptr[i][2] * RADIANS_PER_DEGREE)
            quaternion_list.append(quat_orientation)
        return quaternion_list
# fusiontest.py Simple test program for sensor fusion on Pyboard
# Author Peter Hinch
# Released under the MIT License (MIT)
# Copyright (c) 2017 Peter Hinch
# V0.8 14th May 2017 Option for external switch for cal test. Make platform independent.
# V0.7 25th June 2015 Adapted for new MPU9x50 interface

# import utime as time
import argparse
from fusion import Fusion
import math

parser = argparse.ArgumentParser(description="Integrate accel+gyro+magnet data for the human gait dataset.")
parser.add_argument('--start', default=5, type=int, help='the column of the first accelerometer data')
parser.add_argument('target_file', help='the relative filepath of the file to use')
parser.add_argument('--output_file', help='the relative filepath at which to store the output', default='fusion_output_gait_1.dat')
args = parser.parse_args()

timediff_func = lambda start, end : 33.0/1000

fuse = Fusion(timediff_func)

# Choose test to run
Timing = False

START_COL = args.start
# DEGREES_PER_RADIAN = 360 / (2*math.pi)
DEGREES_PER_RADIAN = 1.0 / (360 / (2*math.pi))

accel_tuples = []
gyro_tuples = []
mag_tuples = []
time_stamps = []

# Starting at column 76 is LUA acc, gyro, mag
with open(args.target_file) as f:
    datalines = f.readlines()[1:] # skip first line (column names)
    curr_time = 0
    for line in datalines:
        datapts = line.split(', ')
        print(datapts[0])
        if datapts[0][0] == '#' or datapts[0] == '' or datapts[0] == '\n':
            continue
        accel = (float(datapts[START_COL]), float(datapts[START_COL+1]), float(datapts[START_COL+2]))
        gyro = (float(datapts[START_COL+3]) * DEGREES_PER_RADIAN, float(datapts[START_COL+4]) * DEGREES_PER_RADIAN, float(datapts[START_COL+5]) * DEGREES_PER_RADIAN)
        mag = (float(datapts[START_COL+6]), float(datapts[START_COL+7]), float(datapts[START_COL+8]))
        curr_time = curr_time + (1.0 / 100) # Assume 100 hz as reported
        timeval = curr_time
        accel_tuples.append(accel)
        gyro_tuples.append(gyro)
        mag_tuples.append(mag)
        time_stamps.append(timeval)
print("Accel tuples length: ", len(accel_tuples))

count = 0
quat_list = []
while count < len(accel_tuples):
    # fuse.update(imu.accel.xyz, imu.gyro.xyz, imu.mag.xyz) # Note blocking mag read
    fuse.update(accel_tuples[count], gyro_tuples[count], mag_tuples[count], time_stamps[count]) # Note blocking mag read
    quat_list.append(fuse.q)
    count += 1

count = 0
with open(args.output_file, "w") as f:
    while count < len(quat_list):
        f.write("{:.3f} {:.3f} {:.3f} {:.3f}\n".format(quat_list[count][0], quat_list[count][1], quat_list[count][2], quat_list[count][3]))
        if count % 50 == 0:
            # print("Heading, Pitch, Roll: {:7.3f} {:7.3f} {:7.3f}".format(fuse.heading, fuse.pitch, fuse.roll))
            print("Quaternion orientation: w={:7.3f} x={:7.3f} y={:7.3f} z={:7.3f}".format(quat_list[count][0], quat_list[count][1], quat_list[count][2], quat_list[count][3]))
        count += 1

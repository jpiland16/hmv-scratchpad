import math
from .DatatypeHandler import DatatypeHandler
from micropython_fusion.fusion import Fusion

DEGREES_PER_RADIAN = 360 / (2*math.pi)
SAMPLE_RATE_HZ = 25.0

class AGMHandler(DatatypeHandler):
    """
    Overriddes parent method. 
    Assumes input data is in the form of nine floats containing accelerometer,
    gyro, and magnetometer data in sequence.
    """
    def get_quaternions(self, data, start_column, time_column):
        fuser = Fusion(lambda start, end : 1.0 / SAMPLE_RATE_HZ)
        accel_tuples = []
        gyro_tuples = []
        mag_tuples = []
        time_stamps = []
        for line in data:
            datapts = line
            if datapts[0] == '#' or datapts[0] == '': # Either remove this, or mention somewhere that lines starting with '#' will be ignored 
                continue
            time_stamps.append(float(datapts[time_column]) / 1000.0)
            accel = (float(datapts[start_column]), float(datapts[start_column+1]), float(datapts[start_column+2]))
            gyro = (float(datapts[start_column+3]), float(datapts[start_column+4]), float(datapts[start_column+5]))
            mag = (float(datapts[start_column+6]), float(datapts[start_column+7]), float(datapts[start_column+8]))
            accel_tuples.append(accel)
            gyro_tuples.append(gyro)
            mag_tuples.append(mag)
        quaternion_list = []
        for count in range(len(accel_tuples)):
            fuser.update(accel_tuples[count], gyro_tuples[count], mag_tuples[count], time_stamps[count]) # Note blocking mag read <- What does this mean?
            quaternion_list.append(fuser.q)
        return quaternion_list
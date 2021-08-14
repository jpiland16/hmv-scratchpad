from ast import parse
import numpy as np
import argparse

START_COLUMN = 76
# START_COLUMN = 0

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--maxlines", "--max", help="Max number of lines to read from the file", type=int)
    args = parser.parse_args()

    total_acc_x = 0
    total_acc_y = 0
    total_acc_z = 0

    lines_read = 0

    with open("data-samples/S1-Drill.dat") as f:
        lines = f.readlines()
        lines = lines[0:args.maxlines] if args.maxlines else lines
        for line in lines:
            datapts = line.split(' ')
            if len(datapts) == 0 or datapts[0] == '#':
                continue
            lines_read += 1
            accX = float(datapts[START_COLUMN])
            accY = float(datapts[START_COLUMN+1])
            accZ = float(datapts[START_COLUMN+2])

            if np.isnan(accX) or np.isnan(accY) or np.isnan(accZ):
                continue
            total_acc_x += accX
            total_acc_y += accY
            total_acc_z += accZ
            print("accX: {0}, accY: {1}, accZ: {2}".format(accX, accY, accZ))
        
    average_acc_x = total_acc_x / lines_read
    average_acc_y = total_acc_y / lines_read
    average_acc_z = total_acc_z / lines_read
    print("Averaged over all lines:\n\taccX: {0}, accY: {1}, accZ: {2}".format(average_acc_x, average_acc_y, average_acc_z))

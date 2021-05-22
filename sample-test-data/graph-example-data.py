import matplotlib.pyplot as plt
import numpy as np

if __name__=='__main__':
    xvals = []
    yvals = []
    with open('output.txt') as f:
        for line in f:
            data_points = line.split(' ')
            xvals.append(float(data_points[4]))
            yvals.append(float(data_points[5]))
    plt.figure()
    plt.plot(xvals, yvals)
    plt.show()
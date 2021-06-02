# Viable candidate datasets
This document lists reasonable target datasets on which to apply the human activity skeleton visualizer:
- [Daily and Sports Activities Data Set](https://archive.ics.uci.edu/ml/datasets/daily+and+sports+activities)
    - It has one unit each for torso, arm and leg. There is accelerometer data, gyro data and magnetometer data. The documentation is fairly sparse but I will look at papers about it.
    - [The paper introducing this dataset](http://kilyos.ee.bilkent.edu.tr/~billur/publ_list/cj14.pdf) shows that it also uses Xsens sensors which is very good news. There's also figures showing the layout of the sensors on the body.

- [A database of human gait performance on irregular and uneven surfaces collected by wearable sensors](https://www.nature.com/articles/s41597-020-0563-y#Sec6)
    - This dataset gives quaternion values from 7 Xsens IMUs placed on wrists, thighs, calves, and the lower back (includes figure showing layout of sensors on the body)

# Criterion for a good dataset
These are listed in descending order of priority and are open to amendment.
- Wearable motion sensors
- Sensors on multiple limbs
- Accelerometer, gyro, magnetometer, or quaternion orientation data
- Diagrams showing local and global coordinate systems
- Diagrams showing layout of sensors on the body
- Activities that could be easily recognized if visualized
- Multiple sensors per limb
- Xsens motion sensors
- Video showing a subject performing the activity during the study

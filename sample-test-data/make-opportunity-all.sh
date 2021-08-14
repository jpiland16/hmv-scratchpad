#!/bin/bash 
# Creates quaternion data from the acc+gyro+mag readings in the opportunity dataset.
input=data-samples/S1-Drill.dat
destination=data-samples/S1-Drill-thirtyseconds-micro-fusioned.dat
python use_datatype_handler_multi.py --degrees --div_factor 1000 $input acc_gyro_mag 37 13 5 $destination
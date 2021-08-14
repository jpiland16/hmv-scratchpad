#!/bin/bash 
# Creates and displays data from the daily+sports dataset.
input=data-samples/barshan-altun-dailysports/raw-data/activity12-subj1-sample6-10.txt
destination=data-samples/barshan-altun-dailysports/processed-data/activity12-subj1-sample6-10-quats.dat
python use-datatype-handler-multi.py --degrees --sep comma $input acc_gyro_mag 27 9 1 $destination
python graph-animate-transf.py --offset 0 $destination
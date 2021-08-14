#!/bin/bash 
# Creates and displays data from the daily+sports dataset.
input=data-samples/barshan-altun-dailysports/raw-data/activity9-subj2-allsamples.txt
destination=data-samples/barshan-altun-dailysports/processed-data/activity9-subj2-allsamples-mfused-quats.dat
python use_datatype_handler_multi.py --degrees --sep comma $input acc_gyro_mag 0 9 5 $destination
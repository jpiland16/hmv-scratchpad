:: Creates and displays data from the daily+sports dataset.
use-datatype-handler-multi.py --degrees --sep comma data-samples/barshan-altun-dailysports/raw-data/activity10-subj1-sample21-22.txt acc_gyro_mag 0 9 1 data-samples/barshan-altun-dailysports/processed-data/activity10-subj1-sample21-22-quats.dat
ECHO =======================
graph-animate-transf.py --offset 0 data-samples/barshan-altun-dailysports/processed-data/activity10-subj1-sample21-quats.dat
PAUSE
:: Creates and displays data from the daily+sports dataset.
set input=data-samples/barshan-altun-dailysports/raw-data/activity10-subj1-sample21-23.txt
set destination=data-samples/barshan-altun-dailysports/processed-data/activity10-subj1-sample21-23-quats.dat
use-datatype-handler-multi.py --degrees --sep comma %input% acc_gyro_mag 27 9 1 %destination%
ECHO =======================
graph-animate-transf.py --offset 0 %destination%
PAUSE
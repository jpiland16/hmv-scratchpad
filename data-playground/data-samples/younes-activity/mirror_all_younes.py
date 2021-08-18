import os
from mirror_file import mirror_file

target_dir_name = 'processed_data'

def handle_file(file_path, activity_id, subject_id, trial_id):
    output_file_name = file_path.replace('processed_data','processed_data_mirrored')
    print("Input file: {0}".format(file_path))
    print("Output file: {0}".format(output_file_name))
    mirror_file(file_path, output_file_name)

count = 0
data_dir = os.walk(target_dir_name)
for dir_name in next(data_dir)[1]:
    activity_id = int(dir_name.split("_")[1])
    activity_dirname = 'processed_data/activity-{0}'.format(activity_id)
    for subj_name in next(os.walk('{0}/{1}'.format(target_dir_name, dir_name)))[1]:
        subj_id = int(subj_name.split("_")[1])    
        subj_dirname = '{0}/subject-{1}'.format(activity_dirname, subj_id)
        for trial_name in next(os.walk('{0}/{1}/{2}'.format(target_dir_name, dir_name, subj_name)))[2]:
            trial_id = int(trial_name.split("_")[2])    
            trial_dirname = '{0}/trial-{1}'.format(subj_dirname, trial_id)
            input_file_name = target_dir_name+'/'+dir_name+'/'+subj_name+'/'+trial_name
            output_file_name = input_file_name.replace('processed_data','processed_data_mirrored')
            print("Copying file:")
            print("Activity id: {0}".format(activity_id))
            print("Subject id: {0}".format(subj_id))
            print("Trial id: {0}".format(trial_id))
            print("================================")
            handle_file(input_file_name, activity_id, subj_id, trial_id)
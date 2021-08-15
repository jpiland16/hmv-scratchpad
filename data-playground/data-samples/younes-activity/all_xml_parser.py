import os
from xml_parser import parse_xml_data

def get_file_meta(file_name):
    parts = file_name.split("_")
    return int(parts[0]), int(parts[1]), int(parts[2].replace('.xml', ''))

count = 0

for item in os.walk('raw_data/xml'):
    for file_name in item[2]:
        print('raw_data/xml/{name}'.format(name=file_name))
        subj_id, activity_id, trial_num = get_file_meta(file_name)
        activity_path = 'processed_data/activity_{0}'.format(activity_id)
        subj_path = 'processed_data/activity_{0}/subj_{1}'.format(activity_id, subj_id)
        if not os.path.isdir(activity_path):
            os.mkdir(activity_path)
        if not os.path.isdir(subj_path):
            os.mkdir(subj_path)
        destination_file_path = '{folder_name}/{file_name}'.format(folder_name=subj_path, file_name=file_name).replace('.xml', '_quats.dat')
        parse_xml_data('raw_data/xml/{name}'.format(name=file_name), destination_file_path)
        count += 1
    print("Finished parsing {num_files} files.".format(num_files=count))
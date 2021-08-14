import os
from use_datatype_handler_multi import process_data

def appended_file(dir_contents):
    for filename in dir_contents:
        if 'appended.txt' in filename:
            return filename
    return None

count = 0
for dir in os.walk('data-samples/gait-data-raw/'):
    if (dir[0] == '.\\__pycache__' or dir[0] == '.'):
        continue
    input_file = appended_file(dir[2])
    if input_file == None:
        continue
    dir_name = dir[0].replace('data-samples/gait-data-raw', '')
    input_filepath = 'data-samples/gait-data-raw/{dir_name}/{file_name}'.format(dir_name=dir_name, file_name=input_file)
    print(input_filepath)
    output_filepath = 'data-samples/gait-data-processed/{filename}'.format(filename=input_file.replace('appended.txt', 'processed.dat'))
    print(output_filepath)
    process_data(input_filepath, 'euler', 21, 30, 6, output_filepath)
    count += 1
    
print("Completed processing {0} files".format(count))
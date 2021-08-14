import os
from append_files_horizontally import append_files

def dir_already_appended(dir_contents):
    for filename in dir_contents:
        if 'appended.txt' in filename:
            return True
    return False

for x in os.walk('.'):
    if len(x[2]) == 0:
        continue
    if (x[0] == '.\\__pycache__' or x[0] == '.'):
        continue
    if dir_already_appended(x[2]):
        continue
    # print(x)
    print(x[0][18:])
    append_files(x[0], "{0}\\subj1_surf{1}_appended.txt".format(x[0],x[0][18:]))
    # if (x[0] == '.\subject1-surface2'):
    #     append_files(x[0], "{0}\\subj1_surf2_appended.txt".format(x[0]))
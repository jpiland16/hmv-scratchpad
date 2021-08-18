def mirror_file(in_filepath, out_filepath, mirror_indices=[1,2,5,6]):
    with open(in_filepath) as in_file:
        with open(out_filepath, 'w') as dest_file:
            for line in in_file.readlines():
                tokens = line.split()
                if len(tokens) == 0:
                    continue
                if  tokens[0] == '#':
                    dest_file.write(line)
                    continue
                line_quats = []
                for i in range(0, len(tokens), 4):
                    curr_quat = []
                    for j in range(4):
                        curr_quat.append(float(tokens[i + j]))
                    line_quats.append(curr_quat)
                # when line quats are done, mirror quats 1,2,5,6
                for index in mirror_indices:
                    mirror_quat = line_quats[index]
                    mirror_quat[0] = mirror_quat[0] * -1
                    mirror_quat[1] = mirror_quat[1] * -1
                for output_quat in line_quats:
                    for num in output_quat:
                        dest_file.write("{0} ".format(num))
                dest_file.write("\n") 

if __name__=="__main__":
    dat_path = 'activity_2/subj_70/70_2_1_quats.dat'
    mirror_file('processed_data/' + dat_path, 'processed_data_mirrored/' + dat_path)
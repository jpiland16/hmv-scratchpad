from datatype_handlers.AccGyroHandler import AGHandler as handler
import os

METADATA = """{"name":"Smartphone Dataset","displayName":"REPLACE_HERE","globalTransformQuaternion":{"x":0,"y":0,"z":0,"w":1},"targets":[{"bone":"ROOT","type":"Quaternion","column":1,"localTransformQuaternion":{"x":0,"y":0,"z":0,"w":1}}]}"""

for TYPE in ["train", "test"]:

    with open("combined_" + TYPE + ".dat", "r") as file:
        data_string = file.read()

    data_lines = data_string.split("\n")
    data = [data_line.split(" ") for data_line in data_lines]

    if not os.path.exists(TYPE):
        os.mkdir(TYPE)

    line_offset = 0
    last_line_offset = 0

    while line_offset < len(data):
        current_subject_index = data[line_offset][7]
        # Go through all of the subjects

        while line_offset < len(data) and data[line_offset][7] == current_subject_index:
            line_offset += 1

        output = handler().get_quaternions(data[last_line_offset:line_offset], 1, 0)

        folder = f"Subject {int(current_subject_index):02}"

        os.mkdir(os.path.join(TYPE, folder))

        with open(os.path.join(TYPE, folder, "quaternion_data.dat"), "w") as file:
            for index, quat in enumerate(output):
                file.write(str(data[index][0]) + " {:.3f} {:.3f} {:.3f} {:.3f}".format(quat[0], quat[1], quat[2], quat[3]) + " " + data[index][7] + " " + data[index][8] + "\n")
                

        with open(os.path.join(TYPE, folder, "metadata.json"), "w") as file:
            file.write(METADATA.replace("REPLACE_HERE", folder))

        print(f"finished converting {TYPE} #{current_subject_index} ({line_offset - last_line_offset} lines)")

        last_line_offset = line_offset
# TYPE = "train"
TYPE = "test"

LABEL_STRINGS = [ "WALKING", "WALKING_UPSTAIRS", "WALKING_DOWNSTAIRS", "SITTING", 
    "STANDING", "LAYING" ]

file_prefixes = ["total_acc", "body_gyro"]
axes = ["_x", "_y", "_z"]
suffix = "_" + TYPE + ".txt"

def do_for_all_files(on_read_file: callable):

    for prefix in file_prefixes:
        for axis in axes:
            file_name = TYPE + "/Inertial Signals/" + prefix + axis + suffix
            with open(file_name, "r") as file:
                on_read_file(file_name, file.read())

def check_lengths():
    file_length = None

    def confirm_file_length(file_name, file_string):
        nonlocal file_length

        if file_length == None:
            file_length = len(file_string.split("\n"))
        else: 
            new_file_length = len(file_string.split("\n"))
            if file_length != new_file_length:
                raise ValueError("Files are not of the same length! " +
                    f"(Last file checked was {file_length} lines long, " +
                    f"{file_name} was {new_file_length} lines long.)")

    do_for_all_files(confirm_file_length)

    return file_length

def concatenate_elementwise(list1, list2):

    if len(list1) != len(list2):
        raise ValueError("Lists are not the same length! " + 
            f"(lengths were {len(list1)} and {len(list2)})")

    return_list = list1[:]

    for index, string in enumerate(list2):
        # Separate using a single space
        return_list[index] += " " + string

    return return_list

def grow_list(my_list, factor):
    """
    Grows a list by the specified factor. 

    Example: [1, 2, 3] * 3 = [1, 1, 1, 2, 2, 2, 3, 3, 3].

    Useful for the fact that the dataset only has one Subject ID and one 
    label (y) for every 128 samples.
    """

    return [item for item in my_list for _ in range(factor)]

def main():
    """
    A note: each line in a ???_?_train.txt file is a 2.56 second window
    consisting of 128 samples (i.e. the sampling rate is 1 sample/0.05 second
    or 20 Hz.)

    Also note, the last line is blank.
    """
    SAMPLES_PER_LINE = 128
    SAMPLE_WINDOW = 2.56 # seconds
    SAMPLE_FREQ = SAMPLES_PER_LINE / SAMPLE_WINDOW

    num_lines = check_lengths()

    # Put time at the beginning of the line
    # Last line is blank
    combined_file_lines = [str(i * SAMPLE_FREQ) for i in range(
        (num_lines - 1) * SAMPLES_PER_LINE)]
    print("# Concatenating (first: line numbers)")

    def concat(file_name, file_string):
        nonlocal combined_file_lines

        # Remove double spaces and spaces at the beginning of a new line
        file_string = file_string.replace("  ", " ").replace("\n ", "\n")
        # The first character is now a single space. Remove that.
        file_string = file_string[1:]

        lines = file_string.split("\n")
        print(f"^ {file_name}")

        combined_file_lines = concatenate_elementwise(
            combined_file_lines,
            # Last line is blank
            [sample for line in lines[:-1] for sample in line.split(" ")]
        )

    do_for_all_files(concat)

    with open(TYPE + "/subject_" + TYPE + ".txt") as file:
        subject_id_string = file.read()

    # Ignore the last line
    subject_ids = subject_id_string.split("\n")[:-1]

    # Grow to correct size
    subject_ids = grow_list(subject_ids, SAMPLES_PER_LINE)

    # Append to existing data
    print("^ subject ids")
    combined_file_lines = concatenate_elementwise(combined_file_lines, 
        subject_ids)

    with open(TYPE + "/y_" + TYPE + ".txt") as file:
        labels_string = file.read()
    
    # ignore the last line
    label_ids = labels_string.split("\n")[:-1]

    # Grow to correct size
    label_ids = grow_list(label_ids, SAMPLES_PER_LINE)

    # Use the labels strings (Note, label_id is 1-indexed and stored as string)
    labels = [LABEL_STRINGS[int(label_id) - 1] for label_id in label_ids]

    # Append to existing data
    print("^ labels")
    combined_file_lines = concatenate_elementwise(combined_file_lines, labels)

    output = "\n".join(combined_file_lines)

    with open("combined_" + TYPE + ".dat", "w") as file:
        file.write(output)

    """
    Output columns:

     0 - Time in milliseconds
     1 - Body acceleration X (in g = 9.81 m/s^2)
     2 - Body acceleration Y (g)
     3 - Body acceleration Z
     4 - Gyro X (rad/s)
     5 - Gyro Y (rad/s)
     6 - Gyro Z (rad/s)
     7 - Subject ID (#1 - 30)
     8 - Label (y --> LABELS)

    """

if __name__ == "__main__":
    main()
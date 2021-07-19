import argparse
from datatype_handlers.EulerAngleHandler import EulerAngleHandler
from datatype_handlers.DeltaQuatHandler import DeltaQuatHandler

data_handlers = {
    'euler': EulerAngleHandler(),
    'delta_q': DeltaQuatHandler()
}


def get_handler(data_type):
    return data_handlers[data_type]


if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Use a datatype handler on a target file")
    parser.add_argument('target_file', help='the file to read')
    parser.add_argument('datatype', help='what type of data to parse', choices=['euler', 'delta_q'])
    parser.add_argument('start_column', type=int, help='the first column of the data (index starts at 0)')
    parser.add_argument('stride_length', type=int, help='the number of columns between the same value in two horizontally appended files')
    parser.add_argument('num_sensors', type=int, help='the number of sensors. number of columns=stride_length*num_sensors')
    parser.add_argument('--time_column', type=int, help='column index for time in millis', default=0)
    parser.add_argument('output_file', help='destination filepath for output quaternions')
    parser.add_argument('--degrees', help='input is degrees instead of radians', action='store_true') # Currently not used. the handler assumes it's degrees...
    args = parser.parse_args()

    with open(args.target_file) as f:
        test_datalines = f.readlines()[1]
        print("num sensors: {0}".format(args.num_sensors))
        print("start column: {0}".format(args.start_column))
        print("stride length: {0}".format(args.stride_length))
        token_list = test_datalines.split()
        print(token_list)
        for i in range(args.num_sensors):
            index = args.start_column + (args.stride_length * i)
            print("target index for token {0}: {1}".format(i, index))
            print("token {0}: {1}".format(i, token_list[args.start_column + (args.stride_length * i)]))

    input_data = []
    with open(args.target_file) as f:
        datalines = f.readlines()[1:] # Skip first line for now
        for line in datalines:
            datapts = line.split() # May want to add optional arg for separator
            input_data.append(datapts)

    output_data = [[] for i in range(len(input_data))]
    for i in range(args.num_sensors):
        handler = get_handler(args.datatype)
        start_column = args.start_column + (i * args.stride_length)
        print("Using handler #{0} with start column {1}".format(i, start_column))
        quat_list = handler.get_quaternions(input_data, start_column, args.time_column)
        for j in range(len(quat_list)):
            output_data[j].extend(quat_list[j])
        
    with open(args.output_file, 'w') as f:
        count = 0
        for line in output_data:
            for data_num in line:
                f.write("{:.3f} ".format(data_num))
            f.write("\n")

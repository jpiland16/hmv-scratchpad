import argparse
from datatype_handlers.EulerAngleHandler import EulerAngleHandler
from datatype_handlers.DeltaQuatHandler import DeltaQuatHandler
from datatype_handlers.AccGyroMagnetHandler import AGMHandler
from datatype_handlers.AccGyroMagnetAltHandler import AGMAltHandler
from datatype_handlers.QuaternionHandler import QuaternionHandler

data_handlers = {
    'euler': EulerAngleHandler(),
    'delta_q': DeltaQuatHandler(),
    'acc_gyro_mag': AGMHandler(),
    'quat': QuaternionHandler()
}

separators = {
    'space': ' ',
    'comma': ','
}


def get_handler(data_type):
    return data_handlers[data_type]

def process_data(target_file, datatype, start_column, stride_length, num_sensors, output_file, time_column=0, degrees=False, sep='space', div_factor=1, start_row=1):
    with open(target_file) as f:
        test_datalines = f.readlines()[1]
        print("num sensors: {0}".format(num_sensors))
        print("start column: {0}".format(start_column))
        print("stride length: {0}".format(stride_length))
        token_list = test_datalines.split(separators[sep])
        print(token_list)
        for i in range(num_sensors):
            index = start_column + (stride_length * i)
            print("target index for token {0}: {1}".format(i, index))
            print("token {0}: {1}".format(i, token_list[start_column + (stride_length * i)]))

    input_data = []
    with open(target_file) as f:
        datalines = f.readlines()[start_row:]
        for line in datalines:
            datapts = line.split(separators[sep]) # May want to add optional arg for separator
            line_data = []
            for data_num in datapts:
                data_num_float = 0
                try:
                    data_num_float = float(data_num) / div_factor
                except ValueError:
                    # print("Encounterd error parsing float value from {str}. Defaulting to 0.".format(str=data_num))
                    pass
                line_data.append(data_num_float)
            input_data.append(line_data)

    print("Number of input data lines: {0}".format(len(input_data)))

    output_data = [[] for i in range(len(input_data))]
    for i in range(num_sensors):
        handler = get_handler(datatype)
        sensor_start_column = start_column + (i * stride_length)
        print("Using handler #{0} with start column {1}".format(i, sensor_start_column))
        quat_list = handler.get_quaternions(input_data, sensor_start_column, time_column)
        for j in range(len(quat_list)):
            output_data[j].extend(quat_list[j])
        
    with open(output_file, 'w') as f:
        count = 0
        for line in output_data:
            for data_num in line:
                f.write("{:.3f} ".format(data_num))
            f.write("\n")


if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Use a datatype handler on a target file")
    parser.add_argument('target_file', help='the file to read')
    parser.add_argument('datatype', help='what type of data to parse', choices=data_handlers.keys())
    parser.add_argument('start_column', type=int, help='the first column of the data (index starts at 0)')
    parser.add_argument('stride_length', type=int, help='the number of columns between the same value in two horizontally appended files')
    parser.add_argument('num_sensors', type=int, help='the number of sensors. number of columns=stride_length*num_sensors')
    parser.add_argument('--time_column', type=int, help='column index for time in millis', default=0)
    parser.add_argument('output_file', help='destination filepath for output quaternions')
    parser.add_argument('--degrees', help='input is degrees instead of radians', action='store_true') # Currently not used. the handler assumes it's degrees...
    parser.add_argument('--sep', help='separator between data points on a line', default='space', choices=separators.keys())
    parser.add_argument('--div_factor', type=int, help='amount by which to divide file data values', default=1)
    parser.add_argument('--start_row', type=int, help='index of the first row to read data from', default=1)
    cl_args = parser.parse_args()
    process_data(cl_args.target_file, cl_args.datatype, cl_args.start_column, cl_args.stride_length, cl_args.num_sensors, cl_args.output_file, cl_args.time_column, cl_args.degrees, cl_args.sep, div_factor=cl_args.div_factor, start_row=cl_args.start_row)

    
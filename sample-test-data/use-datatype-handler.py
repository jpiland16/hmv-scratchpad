import argparse
from datatype_handlers.EulerAngleHandler import EulerAngleHandler

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Use a datatype handler on a target file")
    parser.add_argument('target_file', help='the file to read')
    parser.add_argument('datatype', help='what type of data to parse', choices=['euler'])
    parser.add_argument('start_column', type=int, help='the first column of the data (index starts at 0)')
    parser.add_argument('--time_column', type=int, help='column index for time in millis', default=0)
    parser.add_argument('output_file', help='destination filepath for output quaternions')
    parser.add_argument('--degrees', help='input is degrees instead of radians', action='store_true') # Currently not used. the handler assumes it's degrees...
    args = parser.parse_args()

    handler = EulerAngleHandler()
    input_data = []
    with open(args.target_file) as f:
        datalines = f.readlines()[1:] # Skip first line for now
        for line in datalines:
            datapts = line.split(',')

            input_data.append(datapts)

    print(input_data)
    print(args.start_column)
    print(args.time_column)
    quat_list = handler.get_quaternions(input_data, args.start_column, args.time_column)

    with open(args.output_file, 'w') as f:
        count = 0
        for quat in quat_list:
                f.write("{:.3f} {:.3f} {:.3f} {:.3f}\n".format(quat[0], quat[1], quat[2], quat[3]))
                if count % 50 == 0:
                    print("Quaternion orientation: w={:7.3f} x={:7.3f} y={:7.3f} z={:7.3f}".format(quat[0], quat[1], quat[2], quat[3]))
                count += 1

import argparse
import os

parser = argparse.ArgumentParser(description='appends the files in a directory as if they were all placed next to each other on a page.')
parser.add_argument('target_dir', help='directory in which to horizontally append all files')
parser.add_argument('output_file', help='filepath of output file')
args = parser.parse_args()

def sanitize_line(split_data):
    output_line = []
    for datapt in split_data:
        # if '\n' in datapt or '\r' in datapt:
        #     output_line.append('NONE')
        #     continue
        written_data = datapt.strip() if datapt.strip() != '' else 'NONE'
        output_line.append(written_data)
    return output_line

# Assume the input files all have the same number of rows for now.
# The output should have whitespace separators.
with open(args.output_file, 'w') as dest:
    for filename in os.listdir(args.target_dir):
        with open(os.path.join(args.target_dir, filename), 'r') as f:
            print('Appending {0}'.format(os.path.join(args.target_dir, filename)))
            lines = f.readlines()
            for i in range(len(lines)):
                dest.write(lines[i])
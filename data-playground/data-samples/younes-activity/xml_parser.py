import xml.etree.ElementTree as ET
import argparse


def parse_xml_data(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    quats = {
        'T  ': [],
        'LUA': [], 
        'LFA': [], 
        'RUA': [], 
        'RFA': [],
        'LT ': [],
        'LS ': [],
        'RT ': [],
        'RS ': [],
    }

    for index, frame in enumerate(root[0:]):
        for quaternion in frame[1:]:
            if (quaternion.attrib['name'] not in quats.keys()):
                continue
            curr_quat = [float(quaternion[i].attrib['value']) for i in range(1,5)]
            quats[quaternion.attrib['name']].append(curr_quat)

    print(quats)

    with open(output_file, 'w') as f:
        f.write("# ")
        for key in quats.keys():
            f.write("{0} ".format(key))
        f.write("\n")
        for i in range(len(quats['RUA'])):
            for key in quats.keys():
                try:
                    quat = quats[key][i]
                except IndexError:
                    print("Current joint: {0}. Current index: {1}".format(key, i))
                    raise
                f.write('{:.3f} {:.3f} {:.3f} {:.3f} '.format(quat[0], quat[1], quat[2], quat[3]))
            f.write("\n")

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='XML file with raw quaternion data')
    parser.add_argument('output_file', help='filepath to store output quaternions')
    args = parser.parse_args()
    parse_xml_data(args.input_file, args.output_file)
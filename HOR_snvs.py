import sys
import pickle

def generate_HOR_pattern(read_or):
    HOR_pattern = []
    base_str = '17.mon_'
    if read_or == 1:
        for i in xrange(0,12):
            HOR_pattern += [base_str + str(i)]
    else:
        for i in xrange(11,-1, -1):
            HOR_pattern += [base_str + str(i)]
    return HOR_pattern

def read_input(file_path):
    with open(file_path) as f:
        read = f.readlines()

    monomer_data = []
    ends_data = []
    for line in read:
        eles = line.strip().split()
        ends = (eles[0], eles[1])
        monomer_data += [eles[6]]
        ends_data += [ends]

    return [monomer_data, ends_data]

if __name__ == "__main__":
    read = sys.argv[1].strip().split('/')[2]

    with open('read_orientation.pickle') as f:
        read_orientation = pickle.load(f)

    HOR_pattern = generate_HOR_pattern(read_orientation[read])
    monomer_data, ends_data = read_input(sys.argv[1])

    default_pattern_ends = [(i, i+11) for i in range(len(monomer_data)) if monomer_data[i:i+12] == HOR_pattern]

    if len(default_pattern_ends) != 0:
        print '#####', read, '#####'
        for entry in default_pattern_ends:
            print '~', ends_data[entry[0]][0], ends_data[entry[1]][1]
        print '\n'

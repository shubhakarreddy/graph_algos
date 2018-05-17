##################################################################
# Given the default HOR structure, report all the variations of it
# Input:
# 1. pickle file containing the read sequences
# 2. HOR size -- [int]
##################################################################

import pickle
import sys
import itertools

def generate_kmers(seq, unit_size):
    seq = [str(x) for x in seq]

    kmer_list = []
    for i in xrange(0, len(seq)-unit_size+1):
        kmer_list += ['#'.join(seq[i:i+unit_size])]

    return kmer_list

def checkRotation(seqA, seqB):
    if '#'.join([seqA, seqA]).find(seqB) == -1:
        return False
    return True

with open(sys.argv[1]) as f:
    reads = pickle.load(f)
unit_size = int(sys.argv[2])

total_HOR_units = {}

for read, seq in reads.iteritems():
    kmers = generate_kmers(seq, unit_size)

    detected_HOR_units = []
    HOR_unit_freq = {}
    while len(kmers) > 0:
        HOR = kmers[0]
        marked = {HOR: 1}
        HOR_unit_freq[HOR] = 1

        for kmer in kmers[1:]:
            if kmer in marked:
                HOR_unit_freq[HOR] += 1
            if kmer not in marked and checkRotation(HOR, kmer):
                marked[kmer] = 1
                HOR_unit_freq[HOR] += 1

        for kmer in marked:
            kmers = filter(lambda x: x != kmer, kmers)

    for HOR, freq in HOR_unit_freq.iteritems():
        if HOR in total_HOR_units:
            total_HOR_units[HOR] += freq
        else:
            total_HOR_units[HOR] = freq

HOR_units = total_HOR_units.keys()
while len(HOR_units) > 0:
    HOR = HOR_units[0]
    marked = [HOR]

    for kmer in HOR_units[1:]:
        if checkRotation(HOR, kmer):
            total_HOR_units[HOR] += total_HOR_units[kmer]
            del total_HOR_units[kmer]
            marked += [kmer]

    for kmer in marked:
        HOR_units = filter(lambda x: x != kmer, HOR_units)

for HOR, freq in total_HOR_units.iteritems():
    print freq, HOR.split('#')

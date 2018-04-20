'''
#######################################################
Input:
    1. SAM file
    2. req_aligns pickle file
    3. read sequences -- pickle format
#######################################################
'''

import pysam
import sys
import pickle

def extract_snvs(rname, query_seq, match_tuples):
    snv_set = {}
    ref_seq = read_seqs[rname]
    for match in match_tuples:
        if ref_seq[match[1]] != query_seq[match[0]]:
            snv_set[match[0]] = ref_seq[match[1]]

    return snv_set

if __name__ == '__main__':

    with open(sys.argv[2]) as f:
        global req_aligns = pickle.load(f)

    with open(sys.argv[3]) as f:
        global read_seqs = pickle.load(f)

    samfile = pysam.AlignmentFile(sys.argv[1])

    snv_list = {}
    for alignment in samfile.fetch():
        rstart = alignment.reference_start
        rend = alignment.reference_end
        rname = alignment.reference_name
        mname = alignment.query_name

        uniq_str = '#'.join([str(rstart), str(rend), rname, rend])

        if uniq_str not in req_aligns:
            continue

        match_tuples = alignment.get_aligned_pairs(matches_only=True)
        snv_list[uniq_str] = extract_snvs(rname, alignment.query, match_tuples)

    with open('snv_list.pickle', 'w') as f:
        pickle.dump(snv_list, f)

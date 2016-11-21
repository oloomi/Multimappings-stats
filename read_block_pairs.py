__author__ = 'soloomi'

from collections import defaultdict
from itertools import combinations


def read_pairs(sam_file_path, output_file_path):
    # A dictionary like: {read_id: [list of mapping positions]}
    read_position_dict = defaultdict(list)

    not_mapped_reads = 0  # Number of reads that are not mapped to any location

    # Reading the SAM file and creating a dictionary of read_id : mapping-positions
    with open(sam_file_path) as sam_file:
        for line in sam_file:
            # Skip header lines
            if line[0] == "@":
                continue
            fields = line.rstrip().split("\t")
            read_id = fields[0]  # QNAME: Query template NAME
            cigar = fields[5]  # CIGAR string (ie. alignment)
            pos = int(fields[3])  # 1-based leftmost mapping POSition
            # * means no alignment for a read
            if cigar != "*":
                # How many times a CIGAR string is seen for each read?
                # Store the mapping locations for each CIGAR in a list
                read_position_dict[read_id].append(pos)
            else:
                not_mapped_reads += 1

    # We partition genome to blocks of size 100 bp and we find which block(s) a read maps to
    read_block_dict = defaultdict(list)
    for read, pos_list in read_position_dict.items():
        # if a read maps to multiple positions
        if len(pos_list) > 1:
            for pos in pos_list:
                # It only belongs to one block eg. [101,199] that is block no. 2
                block_no = pos // 100 + 1
                read_block_dict[read].append(block_no)
                # if pos % 100 == 1:
                #     read_block_dict[read].append(block_no)
                # # Otherwise, the read maps to 2 adjacent blocks
                # else:
                #     if block_no > 1:
                #         read_block_dict[read].append(block_no - 1)
                #     read_block_dict[read].append(block_no)

    with open('log-{}'.format(output_file_path), 'w') as log_file:
        for read, block_list in read_block_dict.items():
            log_file.write('{}\n'.format(sorted(block_list)))

    # We find pairs of blocks which share a read
    block_pair_dict = defaultdict(int)
    for read, block_list in read_block_dict.items():
        block_pairs = combinations(block_list, 2)
        for pair in block_pairs:
            block_pair_dict[tuple(sorted(pair))] += 1

    with open(output_file_path, 'w') as block_pair_file:
        for pair_count in sorted(block_pair_dict.items()):
            block_pair_file.write('{}\t{}\t{}\n'.format(pair_count[0][0], pair_count[0][1] , pair_count[1]))

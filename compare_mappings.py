__author__ = 'soloomi'

from collections import defaultdict


def compare_mappings(benchmark_sam_file_name, mapping_sam_file_name, output_file_name):
    # A dictionary like: {read_id: [list of mapping positions]}
    read_position_dict = defaultdict(list)

    not_mapped_reads = 0  # Number of reads that are not mapped to any location

    # Reading the SAM file and creating a dictionary of read_id : mapping-positions
    with open(mapping_sam_file_name) as sam_file:
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

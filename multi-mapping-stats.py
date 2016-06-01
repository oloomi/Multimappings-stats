__author__ = 'soloomi'

from collections import defaultdict


def multi_mapping_stats(sam_file_path, output_file_path):
    # A nested dictionary like: {read_id: {CIGAR: [list of mapping positions]}
    read_cigar_dict = defaultdict(lambda: defaultdict(list))
    not_mapped_reads = 0  # Number of reads that are not mapped to any location

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
                read_cigar_dict[read_id][cigar].append(pos)
            else:
                not_mapped_reads += 1

    # Total number of mapped reads
    total_mapped_reads = len(read_cigar_dict)
    # Number of reads that map only to one location
    unique_reads = 0
    # Number of reads that map to different locations with the same alignment
    same_multi_reads = 0
    # Number of reads that map to different locations with different alignments
    diff_multi_reads = 0

    # For each read
    for read_id, cigar_dict in read_cigar_dict.items():
        # if this read has only one CIGAR
        if len(cigar_dict) == 1:
            # if it has repeated only once, that's a read which maps only to one location
            if len(cigar_dict.values()) == 1:
                unique_reads += 1
            # Otherwise, it maps to more than one location, but with the same alignment
            else:
                same_multi_reads += 1
        else:
            diff_multi_reads += 1

    # Total number of reads
    total_reads = total_mapped_reads + not_mapped_reads

    stats_file = open(output_file_path, 'w')
    stats_file.write('Number of reads that mapped to: \n')
    stats_file.write('- Only one location:\t{}\t{:.2%}\n'.format(unique_reads, unique_reads / total_reads, 3))
    stats_file.write('- More than one location, with the same alignment:'
                     '\t{}\t{:.2%}\n'.format(same_multi_reads, same_multi_reads / total_reads))
    stats_file.write('- More than one location, with different alignments:'
                     '\t{}\t{:.2%}\n'.format(diff_multi_reads, diff_multi_reads / total_reads))
    stats_file.write('Number of reads that did not map to any location:\t{}\t{:.2%}\n'.format(not_mapped_reads,
                                                                                        not_mapped_reads / total_reads))
    stats_file.write('Total number of reads:\t{}\t{:.2%}\n'.format(total_reads, total_reads / total_reads))
    stats_file.write('Total number of mapped reads:\t{}\t{:.2%}\n'.format(total_mapped_reads,
                                                                          total_mapped_reads / total_reads))

    stats_file.close()


multi_mapping_stats("head-mtb-mapping.sam", "mtb-test.txt")
# cigar_counts_stats("mtb-single-mapping-report-all.sam", "mtb-h37rv-single")
# cigar_counts_stats("ot-single-mapping-report-all.sam", "ot-ikeda-single")

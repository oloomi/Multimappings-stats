__author__ = 'soloomi'

from collections import defaultdict

def cigar_counts_stats(sam_file_path, organism):
    # a nested dictionary like: {read_id: {CIGAR: [list of mapping locations]}
    read_cigar_dict = defaultdict(lambda: defaultdict(int))

    sam_file = open(sam_file_path)
    for line in sam_file.readlines():
        # skip header lines
        if line[0] == "@":
            continue
        fields = line.rstrip("\n").split("\t")
        read_id = fields[0]
        cigar = fields[5]
        # * means no alignment for a read
        if cigar != "*":
            # how many times a CIGAR string is seen for each read?
            # store the mapping locations for each CIGAR (ie. alignment) in a list
            read_cigar_dict[read_id][cigar].append(1)

    # total number of reads
    total_reads = len(read_cigar_dict)
    # number of reads that map only to one location
    unique_reads = 0
    # number of reads that map to different locations with the same alignment
    same_multi_reads = 0
    # number of reads that map to different locations with different alignments
    diff_multi_reads = 0

    # for each read
    for read_id, cigar_counts in read_cigar_dict.items():
        # if this read has only one CIGAR
        if len(cigar_counts) == 1:
            # if it has repeated only once, that's a read which maps only to one location
            if sum(cigar_counts.values()) == 1:
                unique_reads += 1
            # Otherwise, it maps to more than one location, but with the same alignment
            else:
                same_multi_reads += 1
        else:
            diff_multi_reads += 1

    cigar_counts_stats_file = open("stats-cigar-counts-{}.txt".format(organism), "w")
    cigar_counts_stats_file.write("#reads that map to only one location:\t{}\t{}\n".
                                  format(unique_reads, round(unique_reads/total_reads, 3)))
    cigar_counts_stats_file.write("#reads that map more than one location, with same CIGAR:\t{}\t{}\n".
                                  format(same_multi_reads, round(same_multi_reads/total_reads, 3)))
    cigar_counts_stats_file.write("#reads that map more than one location, with different CIGAR's:\t{}\t{}\n".
                                  format(diff_multi_reads, round(diff_multi_reads/total_reads, 3)))
    cigar_counts_stats_file.write("#all reads:\t{}\n".format(total_reads))

    cigar_counts_stats_file.close()
    sam_file.close()

cigar_counts_stats("head-mtb-mapping.sam", "mtb-test")
# cigar_counts_stats("mtb-single-mapping-report-all.sam", "mtb-h37rv-single")
# cigar_counts_stats("ot-single-mapping-report-all.sam", "ot-ikeda-single")

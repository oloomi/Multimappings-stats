__author__ = 'soloomi'

from collections import defaultdict


def are_alignments_different(alignments):
    # Check if a multi-read is mapped to different locations with different alignments
    prev_aln = alignments[0][2]  # the MD:Z field
    for aln in alignments[1:]:
        if aln[2] != prev_aln:
            return True
    return False

def compare_mappings(benchmark_sam_file_name, mapping_sam_file_name, output_file_name):
    # A dictionary like: {read_id: [list of mappings CIGAR strings]}
    read_alignments_dict = defaultdict(list)

    not_mapped_reads = 0  # Number of reads that are not mapped to any location

    # Reading the SAM file and creating a dictionary of read_id : alignment
    with open(mapping_sam_file_name) as sam_file:
        for line in sam_file:
            # Skip header lines
            if line[0] == "@":
                continue
            fields = line.rstrip().split("\t")
            read_id = fields[0]  # QNAME: Query template NAME
            cigar = fields[5]  # CIGAR string (ie. alignment)
            pos = int(fields[3])  # 1-based leftmost mapping POSition
            md_z = fields[-2]   # Alignment
            # * means no alignment for a read
            if cigar != "*":
                # Store all alignments of a read
                read_alignments_dict[read_id].append((pos, cigar, md_z))
            else:
                not_mapped_reads += 1

    print("Number of reads not mapped:", not_mapped_reads)

    with open(benchmark_sam_file_name) as sam_file:
        with open(output_file_name, 'w') as out_file:
            line_num = 0
            for line in sam_file:
                # Skip header lines
                if line[0] == "@":
                    continue

                fields = line.rstrip().split("\t")
                read_id = fields[0]  # QNAME: Query template NAME
                cigar = fields[5]  # CIGAR string (ie. alignment)
                pos = int(fields[3])  # 1-based leftmost mapping POSition

                # Add pair suffix to read ID
                line_num += 1
                if line_num % 2 == 0:
                    read_id += "/2"
                else:
                    read_id += "/1"

                # * means no alignment for a read
                if cigar != "*":
                    if read_id in read_alignments_dict and len(read_alignments_dict[read_id]) > 1 and \
                            are_alignments_different(read_alignments_dict[read_id]):
                        out_file.write("{}\t{}\n".format((pos, cigar), read_alignments_dict[read_id]))
                    # else:
                    #     out_file.write("read not found!\n")



compare_mappings("E:\Codes\data\correct-mapping\mtb.sam",
                 "E:\Codes\data\correct-mapping\mtb-single-mapping-report-all.sam", "compared-SAM-mtb.txt")

__author__ = 'soloomi'

from collections import defaultdict
import re
import pysam


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
                    # If we have a multi-read with different alignments
                    if read_id in read_alignments_dict and len(read_alignments_dict[read_id]) > 1 and \
                            are_alignments_different(read_alignments_dict[read_id]):
                        out_file.write("{}\t{}\n".format((pos, cigar), read_alignments_dict[read_id]))
                        # For each mapping position
                        for alignment in read_alignments_dict[read_id]:
                            (pos, cigar, md_z) = alignment

                    # else:
                    #     out_file.write("read not found!\n")


def bases_at_pos(file_name):
    # Opening a BAM file in read mode
    samfile = pysam.AlignmentFile(file_name, "rb")
    # iter = samfile.fetch("gi|448814763|ref|NC_000962.3|", 1000, 2000)
    # GCG
    pileup_iter = samfile.pileup("gi|448814763|ref|NC_000962.3|", 2564751, 2564752)
    for pileup_col in pileup_iter:
        if pileup_col.pos == 2564751:
            print("coverage at base {} = {}".format(pileup_col.pos, pileup_col.n))
            for pileup_read in pileup_col.pileups:
                if not pileup_read.is_del and not pileup_read.is_refskip:
                    print("base in read {} = {}".format(pileup_read.alignment.query_name,
                                                        pileup_read.alignment.query_sequence[pileup_read.query_position]))
    samfile.close()


def mdz_parser(mdz_str):
    """
    Takes the MD:Z filed string and returns a list of SNP positions and the SNP base
    :param mdz_str: the string from MD:Z field of the SAM file for a read
    :return: List of (pos, SNP_base) tuples. Please note that pos is 0-based;
    therefore, pos 0 points to the first base in the sequence.
    """

    # 'MD:Z:15A15A9G15C42'
    # Removing the MD:Z: prefix from the string
    mdz_str = mdz_str[5:]
    # Splitting into alphabetical and numerical parts
    mdz_parsed = filter(None, re.split(r'(\d+)', mdz_str))
    # mdz_parsed = re.findall(r"[^\W\d_]+|\d+", mdz_str)

    # Return list
    pos_snps = []
    pos = 0
    for item in mdz_parsed:
        if item.isalpha():
            for base in item:
                pos_snps.append((pos, base))
                pos += 1
        elif item.isnumeric():
            pos += int(item)
        else:
            print("ERROR: Invalid MD:Z field in SAM file!")

    return pos_snps


print(mdz_parser("MD:Z:G15AT15A9G15C42"))

# bases_at_pos("../data/correct-mapping/mtb-single-mapping-report-all-sorted.bam")

# compare_mappings("E:\Codes\data\correct-mapping\mtb.sam",
#                  "E:\Codes\data\correct-mapping\mtb-single-mapping-report-all.sam", "compared-SAM-mtb.txt")

# compare_mappings("../data/correct-mapping/mtb.sam",
#                  "../data/correct-mapping/mtb-single-mapping-report-all.sam", "compared-SAM-mtb-linux.txt")

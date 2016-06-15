__author__ = 'soloomi'

# import Bio
from Bio import SeqIO, SeqFeature
from collections import defaultdict

def find_annotation(read_cigar_dict, annotation_file, file_format='genbank'):
    """
    Finds the annotation for the locations on the genome where multi-reads map to
    :param read_cigar_dict: a nested dictionary like: {read_id: {CIGAR: [list of mapping positions]}
    :param annotation_file: the path to the reference genome annotation file
    :param file_format: the format of annotation file: 'genbank' or 'fasta'
    """
    position_cigar = defaultdict(list)
    for read_id, cigar_dict in read_cigar_dict.items():
        # if this read has only one CIGAR and has aligned only once; it's a unique read
        if len(cigar_dict) == 1 and len(cigar_dict.values()) == 1:
            # it's not a multi-read
            pass
        else:
            for cigar, positions_list in cigar_dict.items():
                for position in positions_list:
                    # for each position, create a list of read alignments to that location
                    position_cigar[position].append(cigar)


    # print(position_cigar)

    # All locations on the genome which have a multi-read mapped to
    sorted_positions = sorted(position_cigar.keys())


    i = 0
    out_file = open('ot-annotation.txt', 'w')
    record = SeqIO.read(annotation_file, file_format)
    # For each gene, find what multi-reads are in its region, if any
    for feature in record.features:
        if feature.type == 'source':
            continue
        # print(feature.location.start, feature.location.end, feature.location.strand)
        cigars_list = []
        while sorted_positions[i] in range(feature.location.start, feature.location.end + 1):
            cigars_list.append((sorted_positions[i], position_cigar[sorted_positions[i]]))
            if i < len(sorted_positions):
                i += 1
        if cigars_list:
            # print(feature.location.start, '-', feature.location.end, feature.type, cigars_list)
            out_file.write("{}-{} {} {}\n".format(feature.location.start, feature.location.end, feature.type, cigars_list))
    out_file.close()


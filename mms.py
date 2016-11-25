__author__ = 'soloomi'

import argparse
from multi_mappings_statistics import *
from read_block_pairs import *
#from genome_annotation import *

# Getting command line arguments
# parser = argparse.ArgumentParser('Finds multi-mapping statistics')
# parser.add_argument('-i', '--input', required=True, help='The input SAM file that contains read mappings')
# parser.add_argument('-o', '--output', default='output.txt',
#                     help='The output file that will contain multi-mapping statistics')
# args = parser.parse_args()
#
# if args.input:
#     read_cigar_dict = multi_mapping_stats(args.input, args.output)
    # find_annotation(read_cigar_dict, "oti.gb", "genbank")
    # find_annotation(read_cigar_dict, "oti.gb", "genbank")
read_pairs('E:\Codes\data\mtb-single-mapping-report-all.sam', 'block-pairs-mtb-single-10000bp.txt', 10000)
read_pairs('E:\Codes\data\ot-single-mapping-report-all.sam', 'block-pairs-ot-single-10000bp.txt', 10000)

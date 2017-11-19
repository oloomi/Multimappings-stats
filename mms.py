__author__ = 'soloomi'

import argparse
from multi_mappings_statistics import *
from read_block_pairs import *
from merge_blocks import *
from genome_annotation import *
from compare_mappings import compare_mappings

# Getting command line arguments
parser = argparse.ArgumentParser('Finds multi-mapping statistics')
parser.add_argument('-i', '--input', required=True, help='The input SAM file that contains read mappings')
parser.add_argument('-o', '--output', default='output.txt',
                    help='The output file that will contain multi-mapping statistics')
args = parser.parse_args()

if args.input:
    read_cigar_dict = multi_mapping_stats(args.input, args.output)
    find_annotation(read_cigar_dict, "oti.gb", "genbank")
    find_annotation(read_cigar_dict, "oti.gb", "genbank")

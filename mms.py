__author__ = 'soloomi'

import argparse
import multi_mapping_stats

# Getting command line arguments
parser = argparse.ArgumentParser('Finds multi-mapping statistics')
parser.add_argument('-i', '--input', required=True, help='The input SAM file that contains read mappings')
parser.add_argument('-o', '--output', default='output.txt',
                    help='The output file that will contain multi-mapping statistics')
args = parser.parse_args()

if args.input:
    multi_mapping_stats(args.input, args.output)

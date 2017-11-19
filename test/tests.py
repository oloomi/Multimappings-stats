# print(mdz_parser("MD:Z:G15AT15A9G15C40"))
# >> [(0, 'G'), (16, 'A'), (17, 'T'), (33, 'A'), (43, 'G'), (59, 'C')]

# bases_at_pos("../data/correct-mapping/mtb-single-mapping-report-all-sorted.bam", "gi|448814763|ref|NC_000962.3|", 2564751)

# print(bases_at_pos("../data/correct-mapping/single-end-reads/mtb-single-end-mapping-report-all-sorted.bam",
#              "gi|448814763|ref|NC_000962.3|", 4349000))

# compare_mappings("E:\Codes\data\correct-mapping\mtb.sam",
#                  "E:\Codes\data\correct-mapping\mtb-single-mapping-report-all.sam", "compared-SAM-mtb.txt")

# compare_mappings("../data/correct-mapping/mtb.sam",
#                  "../data/correct-mapping/mtb-single-mapping-report-all.sam", "compared-SAM-mtb-linux.txt")

# compare_mappings("gi|448814763|ref|NC_000962.3|", "../data/correct-mapping/mtb.sam",
#                  "../data/correct-mapping/mtb-single-mapping-report-all.sam",
#                  "../data/correct-mapping/mtb-single-mapping-report-all-sorted.bam", "compared-SAM-mtb-SNPs.txt")

# compare_mappings("../data/correct-mapping/test/test-reads.sam",
#                  "../data/correct-mapping/test/test-single-mapping-report-all.sam",
#                  "../data/correct-mapping/test/test-single-mapping-report-all.bam", "compared-test.txt")

# compare_mappings("gi|448814763|ref|NC_000962.3|", "../data/correct-mapping/single-end-reads/mtb/mtb-single-end.sam",
#                  "../data/correct-mapping/single-end-reads/mtb/mtb-single-end-mapping-report-all.sam",
#                  "../data/correct-mapping/single-end-reads/mtb/mtb-single-end-mapping-report-all-sorted.bam",
#                  "compared-mtb-single-reads.txt")

compare_mappings("gi|189182907|ref|NC_010793.1|", "../data/correct-mapping/single-end-reads/mtb/mtb-single-end.sam",
                 "../data/correct-mapping/single-end-reads/mtb/mtb-single-end-mapping-best-match.sam",
                 "../data/correct-mapping/single-end-reads/mtb/mtb-single-end-mapping-report-all.sam",
                 "../data/correct-mapping/single-end-reads/mtb/mtb-single-end-mapping-report-all-sorted.bam",
                 "compared-mtb-single-reads.txt")

# compare_mappings("gi|189182907|ref|NC_010793.1|", "../data/correct-mapping/single-end-reads/ot/ot-single-end.sam",
#                  "../data/correct-mapping/single-end-reads/ot/ot-single-end-mapping-best-match.sam",
#                  "../data/correct-mapping/single-end-reads/ot/ot-single-end-mapping-report-all.sam",
#                  "../data/correct-mapping/single-end-reads/ot/ot-single-end-mapping-report-all-sorted.bam",
#                  "compared-ot-single-reads.txt")

# gi|189182907|ref|NC_010793.1|

# merge_blocks_pairs('sample-blocks-1.txt', 'sample-blocks-1-output.txt')
# merge_blocks_pairs('sample-blocks-2.txt', 'sample-blocks-2-output.txt')
# merge_blocks_pairs('sample-blocks-3.txt', 'sample-blocks-3-output.txt')
merge_blocks_pairs('block-pairs-mtb-single.txt', 'merged-block_pairs_single_mtb.txt')
merge_blocks_pairs('block-pairs-ot-single.txt', 'merged-block_pairs_single_ot.txt')

# read_pairs('E:\Codes\data\mtb-single-mapping-report-all.sam', 'block-pairs-mtb-single-10000bp.txt', 10000)
# read_pairs('E:\Codes\data\ot-single-mapping-report-all.sam', 'block-pairs-ot-single-10000bp.txt', 10000)

merge_blocks('block-pairs-sample-input.txt', 'block-pairs-sample-output.txt')

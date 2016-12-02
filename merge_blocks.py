__author__ = 'soloomi'


def merge_blocks(infile_path, outfile_path):
    # Stack of block pairs and their counts
    pairs_lst = []
    with open(infile_path) as input_file:
        for line in input_file:
            # Input format: block_i block_j Num_of_shared_reads
            current_pair = line.rstrip().split("\t")
            curr_start = int(current_pair[0])
            curr_end = int(current_pair[1])
            curr_count = int(current_pair[2])
            if pairs_lst:
                # Top of the stack
                prev_start = int(pairs_lst[-1][0])
                prev_end = int(pairs_lst[-1][1])
                prev_count = int(pairs_lst[-1][2])

                if curr_start in range(prev_start, prev_start + 2) and curr_end in range(prev_end, prev_end + 2):
                    pairs_lst[-1] = [min(prev_start, curr_start), max(prev_end, curr_end), prev_count + curr_count]
                else:
                    pairs_lst.append([int(i) for i in current_pair])
            else:
                pairs_lst.append([int(i) for i in current_pair])

    with open(outfile_path, 'w') as output_file:
        for pair in pairs_lst:
            output_file.write("{}\t{}\t{}\n".format(pair[0], pair[1], pair[2]))

    return True

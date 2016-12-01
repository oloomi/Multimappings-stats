__author__ = 'soloomi'


def merge_blocks(file_path):
    pairs_lst = []
    with open(file_path) as input_file:
        for line in input_file:
            # Input format: block_i block_j Num_of_shared_reads
            current_pair = line.rstrip().split("\t")
            curr_start = int(current_pair[0])
            curr_end = int(current_pair[1])
            curr_count = int(current_pair[2])
            if pairs_lst:
                prev_start = int(pairs_lst[-1][0])
                prev_end = int(pairs_lst[-1][1])
                prev_count = int(pairs_lst[-1][2])

                if curr_start in range(prev_start, prev_start + 2) and curr_end in range(prev_end, prev_end + 2):
                    pairs_lst[-1] = [min(prev_start, curr_start), max(prev_start, curr_start), prev_count + curr_count]
                else:
                    pairs_lst.append(current_pair)
            else:
                pairs_lst.append(current_pair)

    return True

__author__ = 'soloomi'

def merge_ranges(range_a, range_b):
    """
    Checks whether two ranges are mergeable, and if yes, returns the merged range
    :param range_a: first range
    :param range_b: second range
    :return: If ranges are mergeable, returns the merged range;
    if not, returns None.
    """
    (start_a, end_a) = range_a
    (start_b, end_b) = range_b
    # If two ranges have overlaps, they are mergeable
    #       [A](B) or [A (B ] )                   (B) [A] or (B [A ) ]
    if start_a <= start_b <= end_a + 1 or start_b <= start_a <= end_b + 1:
        return (min(start_a, start_b), max(end_a, end_b))
    else:
        return None

def merge_blocks_pairs(infile_path, outfile_path):
    """
    Merges all block pairs that are adjacent and therefore can be merged into one larger block pair
    :param infile_path: The path to the file with the following format: i m count
    :param outfile_path: The path to the file that the output should be written to
    :return: Writes the output in the file with the following format: i-j  m-n count
    """

    # A semi-merged list of block pairs and sum of their counts, if they are merged
    # [[[x1, x2, y1, y2, count], [x1, x2, y1, y2, count],...], ...]
    pairs_lst = []

    # Reading from file
    with open(infile_path) as input_file:
        for line in input_file:

            # Should have 3 elements: Block_i Block_j num_of_reads i.e. [x, y, count]
            current_pair = list(map(int, line.split()))

            # If the same x as the last pair; i.e. same Block_i to the last one read from file
            if pairs_lst and current_pair[0] == pairs_lst[-1][-1][0]:
                # If current pair is (x, y+1); i.e. their y's are adjacent
                if current_pair[1] == pairs_lst[-1][-1][3] + 1:
                    pairs_lst[-1][-1][3] = current_pair[1]  # Update the range end
                    pairs_lst[-1][-1][4] += current_pair[2] # Add the read count
                # If not, add a new range
                else:
                    pairs_lst[-1].append([current_pair[0], current_pair[0], current_pair[1], current_pair[1],
                                          current_pair[2]])
            # new_x >= last_x
            else:
                # Make a new [[x, x, y, y, count]] and append it
                pairs_lst.append([[current_pair[0], current_pair[0], current_pair[1], current_pair[1],
                                   current_pair[2]]])

    # print(pairs_lst)
    # [
    # [[1, 1, 16, 17, 125], [1, 1, 55, 56, 87]],
    # [[2, 2, 18, 19, 31], [2, 2, 56, 56, 14]]
    # ]


    prev = pairs_lst[0]
    # Final outcome which contains the lists of list of merged block pairs
    results = [prev[:]]
    list_index = 1
    # For each list of semi-merged block pairs e.g. [[x1, x2, y1, y2, count], [x1, x2, y1, y2, count],...]
    while list_index < len(pairs_lst):
        curr = pairs_lst[list_index]
        i = 0
        j = 0
        # If the x's in the current list is adjacent to the x's in the previous list
        if prev[0][1] <= curr[0][0] <= prev[0][1] + 1:
            # Indices of those items in the previous list which has been merged with an item in the current list
            used_prevs = []
            # For each item in curr list:
            while i < len(curr):
                j = 0
                # Check it against each item in prev list to see if they can be merged together
                while j < len(prev):
                    # Skip those which have already been merged
                    if j in used_prevs:
                        j += 1
                        continue
                    # (prev_start, prev_end)
                    prev_range = (prev[j][2], prev[j][3])   # (16, 17)
                    # (curr_start, curr_end)
                    curr_range = (curr[i][2], curr[i][3])   # (18, 19)

                    merged_range = merge_ranges(prev_range, curr_range)

                    # If we can merge two ranges:
                    if merged_range:
                        # Find the merged range
                        # [1, 2, 16, 19, c1 + c2]
                        curr[i] = [min(prev[j][0], curr[i][0]), max(prev[j][1], curr[i][1]),
                                   merged_range[0], merged_range[1], prev[j][4] + curr[i][4]]

                        # Check if the new (merged) range can be merged with the previous items in curr
                        while i > 0:
                            last_item = curr[i-1]
                            merged_with_last_item = merge_ranges((last_item[2], last_item[3]), (curr[i][2], curr[i][3]))
                            if merged_with_last_item:
                                new_curr_item = [min(last_item[0], curr[i][0]), max(last_item[1], curr[i][1]),
                                                 merged_with_last_item[0], merged_with_last_item[1],
                                                 last_item[4] + curr[i][4]]
                                curr[i-1] = new_curr_item   # Update the preceding item
                                curr.pop(i)     # Remove the item that has been just merged with the preceding item
                                i -= 1
                            else:
                                break

                        # Check if the new range can be merged with the next items in curr
                        while True:
                            if i < (len(curr) - 1):
                                next_item = curr[i+1]
                                merged_with_next_item = merge_ranges((next_item[2], next_item[3]),
                                                                     (curr[i][2], curr[i][3]))
                                if merged_with_next_item:
                                    new_curr_item = [min(next_item[0], curr[i][0]), max(next_item[1], curr[i][1]),
                                                     merged_with_next_item[0], merged_with_next_item[1],
                                                     next_item[4] + curr[i][4]]
                                    curr[i+1] = new_curr_item   # Update the succeeding item
                                    curr.pop(i)
                                    if i > 0:
                                        i -= 1
                                    else:
                                        break
                                else:
                                    break
                            else:
                                break

                        # After an item in curr has been merged with an item in prev
                        used_prevs.append(j)
                        # Move on to the next item in curr
                        break
                    else:
                        j += 1
                # Moving on to the next item in curr
                i += 1
            # When all items in curr have been checked for merging and mergings are done with curr
            if used_prevs:
                # Remove those items from results[-1] i.e. prev that have been merged now with items in current list
                for lst_index in sorted(used_prevs, reverse=True):
                    results[-1].pop(lst_index)
            # Add curr to the list of results
            results.append(curr)
        else:
            # curr can not be merged further, just add it to the list of results
            results.append(curr)

        prev = curr
        list_index += 1
    # End of merging block pairs

    # print("Merged ranges: ")
    with open(outfile_path, 'w') as outfile:
        for lst in results:
            for pair in lst:
                # print("{}-{}\t{}-{}\t{}".format(pair[0], pair[1], pair[2], pair[3], pair[4]))
                outfile.write("{}-{}\t{}-{}\t{}\n".format(pair[0], pair[1], pair[2], pair[3], pair[4]))

    print("Done!")

# merge_blocks_pairs('sample-blocks-1.txt', 'sample-blocks-1-output.txt')
# merge_blocks_pairs('sample-blocks-2.txt', 'sample-blocks-2-output.txt')
# merge_blocks_pairs('sample-blocks-3.txt', 'sample-blocks-3-output.txt')
merge_blocks_pairs('block-pairs-mtb-single.txt', 'merged-block_pairs_single_mtb.txt')
merge_blocks_pairs('block-pairs-ot-single.txt', 'merged-block_pairs_single_ot.txt')

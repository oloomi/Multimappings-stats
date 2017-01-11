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

def merge_ranges(range_a, range_b):
    (start_a, end_a) = range_a
    (start_b, end_b) = range_b
    #       [A](B) or [A (B ] )                   (B) [A] or (B [A ) ]
    if start_a <= start_b <= end_a + 1 or start_b <= start_a <= end_b + 1:
        return (min(start_a, start_b), max(end_a, end_b))
    else:
        return None

def merge_blocks_pairs(infile_path, outfile_path):
    # A semi-merged list of block pairs
    # [[[x1, x2, y1, y2], [x1, x2, y1, y2],...], ...]
    pairs_lst = []
    # Reading from file
    with open(infile_path) as input_file:
        for line in input_file:
            current_pair = list(map(int, line.split()))
            # If the same x as the last pair
            if pairs_lst and current_pair[0] == pairs_lst[-1][-1][0]:
                # If current pair is (x, y+1)
                if current_pair[1] == pairs_lst[-1][-1][3] + 1:
                    pairs_lst[-1][-1][3] = current_pair[1]  # Update the range end
                # Add a new range
                else:
                    pairs_lst[-1].append([current_pair[0], current_pair[0], current_pair[1], current_pair[1]])
            else:
                # Make a new [x, x, y, y] and append it
                pairs_lst.append([[current_pair[0], current_pair[0], current_pair[1], current_pair[1]]])

    print(pairs_lst)
    # [
    # [[1, 1, 16, 17], [1, 1, 55, 56]],
    # [[2, 2, 18, 19], [2, 2, 56, 56]]
    # ]

    prev = pairs_lst[0]
    results = [prev[:]]
    list_index = 1
    while list_index < len(pairs_lst):
        curr = pairs_lst[list_index]
        i = 0
        j = 0
        #
        if prev[0][1] <= curr[0][0] <= prev[0][1] + 1:
            used_prevs = []
            # For each item in curr list:
            while i < len(curr):
                j = 0
                # Check it against each item in prev list to see if they can be merged together
                while j < len(prev):
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
                        curr[i] = [min(prev[j][0], curr[i][0]), max(prev[j][1], curr[i][1]),
                                   merged_range[0], merged_range[1]]    # [1, 2, 16, 19]
                        # if results:
                        #     results[-1].pop(j)

                        # Check if the new range can be merged with the previous items in current
                        while i > 0:
                            last_item = curr[i-1]
                            merged_with_last_item = merge_ranges((last_item[2], last_item[3]), (curr[i][2], curr[i][3]))
                            if merged_with_last_item:
                                new_curr_item = [min(last_item[0], curr[i][0]), max(last_item[1], curr[i][1]),
                                                 merged_with_last_item[0], merged_with_last_item[1]]
                                curr[i-1] = new_curr_item
                                curr.pop(i)
                                i -= 1
                            else:
                                break

                        # Check if the new range can be merged with the next items in current
                        while True:
                            if i < (len(curr) - 1):
                                next_item = curr[i+1]
                                merged_with_next_item = merge_ranges((next_item[2], next_item[3]), (curr[i][2], curr[i][3]))
                                if merged_with_next_item:
                                    new_curr_item = [min(next_item[0], curr[i][0]), max(next_item[1], curr[i][1]),
                                                     merged_with_next_item[0], merged_with_next_item[1]]
                                    curr[i+1] = new_curr_item
                                    curr.pop(i)
                                    if i > 0:
                                        i -= 1
                                    else:
                                        break
                                else:
                                    break
                            else:
                                break

                        used_prevs.append(j)
                        break
                    else:
                        j += 1
                i += 1
            # print(curr)
            if used_prevs:
                # remove those items from results[-1] i.e. prev that have been merged now with items in current list
                for lst_index in sorted(used_prevs, reverse=True):
                    results[-1].pop(lst_index)
            results.append(curr)
        else:
            # print(curr)
            results.append(curr)

        prev = curr
        list_index += 1

    print("Merged ranges: ")
    with open(outfile_path, 'w') as outfile:
        for lst in results:
            for pair in lst:
                print("{}-{}\t{}-{}".format(pair[0], pair[1], pair[2], pair[3]))
                outfile.write("{}-{}\t{}-{}\n".format(pair[0], pair[1], pair[2], pair[3]))







# def group(xys):
#     grp = []
#     for (x, y) in xys:
#         if len(grp) > 0 and grp[0][0] != x:
#             yield grp
#             grp = []
#         grp.append((x, y))
#     if len(grp) > 0:
#         yield grp
#
# def findAliases(xs):
#     live = []
#     for grp in group(xs):
#         x = grp[0][0]
#         keep = []
#         used = set([])
#         for v in live:
#             if v[0] != x and v[0] + 1 != x:
#                 yield v
#                 continue
#             found = False
#             for i in range(len(grp)):
#                 if i in used:
#                     continue
#                 blk = grp[i]
#                 y = blk[1]
#                 if v[1] == y or v[1] + 1 == y:
#                     used.add(i)
#                     v[0] = x
#                     v[1] = y
#                     keep.append(v)
#                     found = True
#                     break
#             if not found:
#                 yield v
#         live = keep
#         for i in range(len(grp)):
#             if i in used:
#                 continue
#             y = grp[i][1]
#             live.append([x, y, x, y, None])
#     for v in live:
#         yield v

# xs = []
# for l in sys.stdin:
#     t = l.split()
#     xs.append(map(int, t))
# with open('sample-blocks.txt') as input_file:
#     for line in input_file:
#         t = line.split()
#         xs.append(map(int, t))
#
# for v in findAliases(xs):
#     print(v)

merge_blocks_pairs('sample-blocks.txt', 'output.txt')
merge_blocks_pairs('sample-blocks-2.txt', 'sample-blocks-2-output.txt')
merge_blocks_pairs('sample-blocks-3.txt', 'sample-blocks-3-output.txt')
# merge_blocks_pairs('block-pairs-mtb-single.txt', 'mtb-merged-output.txt')

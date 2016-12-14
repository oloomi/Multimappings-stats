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
    # [[2, 2, 17, 18], [2, 2, 56, 56]]
    # ]
    prev = pairs_lst[0]
    list_index = 1
    while list_index < len(pairs_lst):
        curr = pairs_lst[list_index]
        i = 0
        j = 0
        #
        if curr[0][0] == prev[0][1] + 1:
            while i < len(curr) and j < len(prev):
                (prev_start, prev_end) = (prev[j][2], prev[j][3])
                (curr_start, curr_end) = (curr[i][2], curr[i][3])
                if prev_end <= curr_start <= prev_end + 1:
                    # print(prev[j][0], curr[i][1], prev_start, curr_end)
                    curr[i] = [prev[j][0], curr[i][1], prev_start, curr_end]
                    i += 1
                    j += 1
                elif prev_start <= curr_end <= prev_start + 1:
                    # print(prev[j][0], curr[i][1], curr_start, prev_end)
                    curr[i] = [prev[j][0], curr[i][1], prev_start, curr_end]
                    i += 1
                    j += 1
                else:
                    i += 1
            print(curr)
        else:
            print(curr)

        prev = curr
        list_index += 1






def group(xys):
    grp = []
    for (x, y) in xys:
        if len(grp) > 0 and grp[0][0] != x:
            yield grp
            grp = []
        grp.append((x, y))
    if len(grp) > 0:
        yield grp

def findAliases(xs):
    live = []
    for grp in group(xs):
        x = grp[0][0]
        keep = []
        used = set([])
        for v in live:
            if v[0] != x and v[0] + 1 != x:
                yield v
                continue
            found = False
            for i in range(len(grp)):
                if i in used:
                    continue
                blk = grp[i]
                y = blk[1]
                if v[1] == y or v[1] + 1 == y:
                    used.add(i)
                    v[0] = x
                    v[1] = y
                    keep.append(v)
                    found = True
                    break
            if not found:
                yield v
        live = keep
        for i in range(len(grp)):
            if i in used:
                continue
            y = grp[i][1]
            live.append([x, y, x, y, None])
    for v in live:
        yield v

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

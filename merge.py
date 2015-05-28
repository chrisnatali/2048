"""
Module for merge function in 2048 game
"""

def _find_adjacent(i, line):
    """
    find the indices of the next set of adjacent 2048 numbers in the list

    Args:
        i: start index of the "left" value
        line:  the list of 2048 numbers

    Returns:
        i, j:  indices of the next adjacent numbers in the list
            if there are no more adjacent numbers left i will be
            len(line) - 1

    """

    # find the next non zero i
    while i < (len(line) - 1) and line[i] == 0:
        i += 1

    j = i + 1
    # find the next non zero j after i
    while j < len(line) and line[j] == 0:
        j += 1

    return i, j
        
def merge(line):
    """
    Merge the tiles in a line of 2048

    Assumes the line should be merged left (0) to right (len(line))

    Args:
        line:  a line of 2048 numbers
    """
    
    result = [0] * len(line)
    current = i = 0

    # find adjacent elements adding them when they match
    # or just inserting the next item when they don't
    while i < len(line):
        i, j = _find_adjacent(i, line)
        # when j is beyond list end, no need to test
        if j < len(line) and line[i] == line[j]:
            result[current] = line[i] + line[j]
            i = j + 1
        else:
            result[current] = line[i]
            i = j

        current +=1

    # the rest of result have already been filled in with 0's
    # so we're done

    return result

def test_merge():
    """
    generate random 2048 line of length 20 and ensure that all 0's are
    to the right and the correct number of matching pairs are merged
    """
    import random
    line = [random.choice([0,2,4,8]) for i in range(20)]
    # ensure that there's at least one merged pair (3,5) and that
    # not all results are 0
    line[2:6] = [4, 2, 0, 2]

    result = merge(line)
    merged_pairs = []
    i = 0
    while True:
        while i < (len(line) - 1) and line[i] == 0: 
            i += 1

        if not i < (len(line) - 1):
            break

        j = i + 1
        while j < len(line) and line[j] == 0: 
            j += 1

        if not j < len(line): 
            break

        if line[i] == line[j]:
            merged_pairs.append((i, j))
            i = j + 1
        else:
            i = j

    def get_state():
       return "line {}\nresult {}\nmerged {}".format(line, 
                                                     result, 
                                                     merged_pairs)

    # check for known merged pair
    assert filter(lambda pair: pair == (3, 5), merged_pairs),\
        "merged pair (3, 5) not found\n{}".format(get_state())

    # check appropriate number of zeros to the right
    zero_size = len(filter(lambda x: x == 0, line)) + len(merged_pairs)
    assert result[-(zero_size):] == [0] * zero_size,\
        "wrong number of zeros {} on right side\n{}".format(zero_size, 
                                                            get_state())

    # check numbers to the left are non zero
    left_side = result[:(len(line) - zero_size)]
    assert len(filter(lambda x: x == 0, left_side)) == 0,\
        "left side {} contains zeros\n{}".format(left_side, 
                                                 get_state())

"""
Module for merge function in 2048 game
"""

def find_adjacent(left, line):
    """
    find the indices of the next set of adjacent 2048 numbers in the list

    Args:
        left: start index of the "left" value
        line:  the list of 2048 numbers

    Returns:
        left, right:  indices of the next adjacent numbers in the list
            if there are no more adjacent numbers, left will be
            len(line) - 1

    """

    # find the next non zero index for left
    while left < (len(line) - 1) and line[left] == 0:
        left += 1

    right = left + 1
    # find the next non zero index after left
    while right < len(line) and line[right] == 0:
        right += 1

    return left, right 
        

def merge(line):
    """
    Merge the tiles in a line of 2048

    Assumes the line should be merged left (0) to right (len(line))

    Args:
        line:  a line of 2048 numbers
    """
    
    result = [0] * len(line)
    current = left = 0

    # find adjacent elements adding them when they match
    # or just inserting the next item when they don't
    while left < len(line):
        left, right = find_adjacent(left, line)
        # when right is beyond list end, no need to test
        if right < len(line) and line[left] == line[right]:
            result[current] = line[left] + line[right]
            left = right + 1
        else:
            result[current] = line[left]
            left = right 

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
    line = [random.choice([0,2,4,8]) for _ in range(20)]
    # ensure that there's at least one merged pair (3,5) and that
    # not all results are 0
    line[2:6] = [4, 2, 0, 2]

    result = merge(line)
    merged_pairs = []
    left = 0
    while True:
        while left < (len(line) - 1) and line[left] == 0: 
            left += 1

        if not left < (len(line) - 1):
            break

        right = left + 1
        while right < len(line) and line[right] == 0: 
            right += 1

        if not right < len(line): 
            break

        if line[left] == line[right]:
            merged_pairs.append((left, right))
            left = right + 1
        else:
            left = right

    def get_state():
        """ Get string representing state needed for debugging """
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

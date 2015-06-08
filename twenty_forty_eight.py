"""
Clone of 2048 game.
"""

import random
# import poc_2048_gui

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


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


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        """
        initialize grid of height, width
        """
        self.height = grid_height
        self.width = grid_width
        # initial tiles for direction from which to traverse
        self.initial_tiles = {
                UP: [(0, col) for col in range(self.width)], 
                DOWN: [(self.height - 1, col) for col in range(self.width)],
                LEFT: [(row, 0) for row in range(self.height)],
                RIGHT: [(row, self.width - 1) for row in range(self.height)]
                }

        # number of tiles to traverse per direction
        self.num_tiles = {
                UP: self.height, 
                DOWN: self.height,
                LEFT: self.width,
                RIGHT: self.width
                }

        self.reset()


    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self.grid = [[0 for col in range(self.width)]
                    for row in range(self.height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        strings = [[str(val) for val in row] for row in self.grid]
        # get max len per column for alignment 
        lens = [max(map(len, col)) for col in zip(*strings)]
        # create a format string for each column
        fmt = ','.join('{{:{}}}'.format(length) for length in lens)
        # apply format to each column in each row
        table = [fmt.format(*row) for row in strings]
        return '\n'.join(table)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # iterate over all initial tiles for the direction
        # merge the line associated with the initial tile
        # and put it back in the grid
        for start in self.initial_tiles[direction]:
            # to keep track of tiles associated with line elements
            line_grid_map = {}
            line = []
            cur = start
            for index in range(self.num_tiles[direction]):
                line_grid_map[index] = cur
                line.append(self.get_tile(*cur))
                # update row and col
                row = cur[0] + OFFSETS[direction][0]
                col = cur[1] + OFFSETS[direction][1]
                cur = (row, col)

            merged = merge(line)
            for index in range(self.num_tiles[direction]):
                row, col = line_grid_map[index]
                self.set_tile(row, col, merged[index])


    def _empty_tiles(self):
        """
        return tiles (as tuples) that are empty
        """
        tuples = []
        for row in range(self.height):
            for col in range(self.width):
                if self.grid[row][col] == 0:
                    tuples.append((row, col))

        return tuples


    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # get empty tiles 
        empties = self._empty_tiles()
        # create distribution from which to choose value
        value_distribution = [4,2,2,2,2,2,2,2,2,2]
        if len(empties) > 0:
            row, col = random.choice(empties)
            val = random.choice(value_distribution)
            self.set_tile(row, col, val)


    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self.grid[row][col]

# poc_2048_gui.run_gui(TwentyFortyEight(4, 4))


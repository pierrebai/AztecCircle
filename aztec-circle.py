from random import Random

class repeatable_random:
    """
    A random number generator that can be rewind to replay the same random sequence.
    """

    _save_period = 1000

    def __init__(self, seed_value: int):
        """
        Create a repeatable random generator with the given seed.
        """
        self._rnd = Random(seed_value)
        self._count = 0
        self._states = []
        self._save_regularly()

    def next(self) -> bool:
        """
        Save or restore the random state then generates the next random boolean.
        """
        self._save_regularly()
        self._count += 1
        return self._rnd.randrange(2) == 1

    def rewind(self, amount: int = 1):
        """
        Rewind the random generator the given number of values.
        Default to rewinding a single value.
        Rewinding a negative amount goes forward instead.
        """
        target_count = max(0, self._count - amount)
        state_index = min(target_count // repeatable_random._save_period, len(self._states) - 1)
        self._rnd.setstate(self._states[state_index])
        self._count = state_index * repeatable_random._save_period
        while self._count != target_count:
            self.next()

    def _save_regularly(self):
        """
        Regularly save the state of the random number generator
        so that we can go back in time.
        Restore the state if we went back to a previous already-genarated
        value.
        """
        if self._count % repeatable_random._save_period == 0:
            state_index = self._count // repeatable_random._save_period
            while state_index < len(self._states):
                self._states.append(self._rnd.getstate())


class tile:
    def __init__(self, is_horizontal: bool, is_positive: bool):
        self.is_horizontal = is_horizontal
        self.is_positive = is_positive

    def grow_pos(self, pos: tuple):
        if self.is_horizontal:
            if self.is_positive:
                return (pos[0], pos[1]+1)
            else:
                return (pos[0], pos[1]-1)
        else:
            if self.is_positive:
                return (pos[0]+1, pos[1])
            else:
                return (pos[0]-1, pos[1])

class aztec:
    def __init__(self, target_size: int, seed: int):
        """
        Create a filled aztec diamond of the given size.
        """
        self._size = 0
        self._tiles = {}
        self._rnd = repeatable_random(seed)
        self.grow_to_size(target_size)

    def grow_to_size(self, target_size: int):
        """
        Grow the aztec diamond to the given size.
        Does nothing if the target size is smaller.
        TODO: allow rewinding to a smaller size.
        """
        while self._size < target_size:
            self.grow()

    def grow(self):
        self._size += 1
        self._remove_collisions()
        self._recenter()
        self._move_tiles()
        self._fill_holes()

    def size(self) -> int:
        return self._size

    def tiles(self) -> dict:
        return self._tiles

    def _remove_collisions(self):
        new_tiles = self._tiles.copy()
        for pos, tile in self._tiles.items():
            other_pos = tile.grow_pos(pos)
            if other_pos not in new_tiles:
                continue
            other_tile = new_tiles[other_pos]
            if other_tile.is_positive != tile.is_positive and other_tile.is_horizontal == tile.is_horizontal:
                del new_tiles[pos]
                del new_tiles[other_pos]
        self._tiles = new_tiles

    def _recenter(self):
        if not self._tiles:
            return
        new_tiles = {}
        for pos, tile in self._tiles.items():
            new_tiles[(pos[0]+1, pos[1]+1)] = tile
        self._tiles = new_tiles

    def _move_tiles(self):
        new_tiles = {}
        for pos, tile in self._tiles.items():
            new_pos = tile.grow_pos(pos)
            new_tiles[new_pos] = tile
        self._tiles = new_tiles

    @staticmethod
    def is_corner(x: int, y: int, size: int) -> bool:
        if x >= size:
            x = (size * 2 - 1) - x
        if y >= size:
            y = (size * 2 - 1) - y
        return x + y < size - 1

    def _noop(self):
        pass

    def _fill_holes(self):
        double_size = self._size * 2
        for x in range(0, double_size - 1):
            for y in range(0, double_size - 1):
                if aztec.is_corner(x, y, self._size):
                    continue
                if aztec.is_corner(x+1, y+1, self._size):
                    continue
                if (x,y) in self._tiles:
                    continue
                if (x+1,y) in self._tiles:
                    continue
                if (x,y+1) in self._tiles:
                    continue
                if (x+1,y+1) in self._tiles:
                    continue
                is_horizontal = self._rnd.next()
                if is_horizontal:
                    self._tiles[(x,   y  )] = \
                    self._tiles[(x+1, y  )] = tile(is_horizontal, False)
                    self._tiles[(x  , y+1)] = \
                    self._tiles[(x+1, y+1)] = tile(is_horizontal, True)
                else:
                    self._tiles[(x  , y  )] = \
                    self._tiles[(x  , y+1)] = tile(is_horizontal, False)
                    self._tiles[(x+1, y  )] = \
                    self._tiles[(x+1, y+1)] = tile(is_horizontal, True)


def needs_separator(tiles: dict, pos1: tuple, pos2: tuple) -> int:
    """
    0: empty separator
    1: separator
    2: linked half-tiles separator
    """
    if pos1 in tiles and pos2 in tiles:
        return [1, 2][tiles[pos1] == tiles[pos2]]
    else:
        return [0, 1][pos1 in tiles or pos2 in tiles]

def draw_inter_horizontal(tiles: dict, pos1: tuple, pos2: tuple, line: list):
    line.append([' ', '|', ' '][needs_separator(tiles, pos1, pos2)])

def draw_inter_horizontal_for_vertical(tiles: dict, x: int, y: int, line: list):
    horiz_sep = max(needs_separator(tiles, (x-1, y  ), (x  , y  )),
                    needs_separator(tiles, (x-1, y+1), (x  , y+1)))
    verti_sep = max(needs_separator(tiles, (x-1, y  ), (x-1, y+1)),
                    needs_separator(tiles, (x  , y  ), (x  , y+1)))
    if horiz_sep == 2:
        line.append('-')
    elif verti_sep == 2:
        line.append('|')
    elif horiz_sep == 1 or verti_sep == 1:
        line.append('+')
    else:
        line.append(' ')

def draw_inter_verticals(tiles: dict, y: int, size: int):
    line = []
    for x in range(0, size * 2):
        draw_inter_horizontal_for_vertical(tiles, x, y, line)
        draw_inter_vertical(tiles, (x, y), (x, y+1), line)
    draw_inter_horizontal_for_vertical(tiles, x+1, y, line)
    print(''.join(line))

def draw_inter_vertical(tiles: dict, pos1: tuple, pos2: tuple, line):
    line.append(['   ', '---', '   '][needs_separator(tiles, pos1, pos2)])

def draw_aztec_ascii(az: aztec):
    tile_colors = [ ['Y', 'R'], ['B', 'G'] ]
    tiles = az.tiles()
    for y in range(0, az.size() * 2):
        draw_inter_verticals(tiles, y-1, az.size())
        line = []
        for x in range(0, az.size() * 2):
            pos = (x, y)
            draw_inter_horizontal(tiles, (x-1, y), pos, line)
            if pos not in tiles:
                line.append('   ')
            else:
                tile = tiles[pos]
                color = tile_colors[tile.is_horizontal][tile.is_positive]
                line.append(f' {color} ')
        draw_inter_horizontal(tiles, (x, y), (x+1, y), line)
        print(''.join(line))
    draw_inter_verticals(tiles, y, az.size())

seed = 7
az = aztec(0, seed)
for i in range(0, 10):
    az.grow()
    draw_aztec_ascii(az)
    print('')
    print('')


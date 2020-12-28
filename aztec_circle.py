from half_tile import available_tiles
from reactor import reactor

class aztec:
    """
    Aztec artic circle tiling, as per the Mathologer you-tube video.
    """

    def __init__(self, target_size: int, tile_generator, react = reactor()):
        """
        Create a filled aztec diamond of the given size.
        """
        self._size = 0

        self.tile_generator = tile_generator
        self.reactor = react

        self._squares = []
        self._tmp_squares = []
        self._origin = 0
        self._allocate_tiles(100)

        self.grow_to_size(target_size)

    def _allocate_tiles(self, amount: int):
        if amount % 2:
            amount += 1

        old_amount = len(self._squares)
        if amount < old_amount:
            return

        skip, self._squares, self._tmp_squares = aztec.reallocate_data(old_amount, amount, self._squares, self._tmp_squares)
        self._origin += skip
        self.reactor.reallocate(self, old_amount, amount)

    @staticmethod
    def reallocate_data(old_amount: int, new_amount: int, old_data: list, old_tmp: list):
        skip = (new_amount - old_amount) // 2

        new_squares = []
        new_tmp_squares = []

        for i in range(0, skip):
            new_squares.append([ None ] * new_amount)
            new_tmp_squares.append([ None ] * new_amount)

        for old_line in old_data:
            line = [ None ] * skip
            line.extend(old_line)
            line.extend([ None ] * skip)
            new_squares.append(line)
            new_tmp_squares.append([ None ] * new_amount)

        for i in range(0, skip):
            new_squares.append([ None ] * new_amount)
            new_tmp_squares.append([ None ] * new_amount)

        return skip, new_squares, new_tmp_squares

    def grow_to_size(self, target_size: int):
        """
        Grow the aztec diamond to the given size.
        Does nothing if the target size is smaller.
        TODO: allow rewinding to a smaller size.
        """
        while self._size < target_size:
            self.grow()

    def grow(self):
        """
        Grow the aztec diamond size by one.
        """
        self.reactor.start_grow(self)
        self.increase_size()
        self.remove_collisions()
        self.move_tiles()
        self.fill_holes()
        self.reactor.end_grow(self)

    def size(self) -> int:
        """
        Return the size of the aztec diamond.
        """
        return self._size

    def center(self) -> int:
        """
        Return the coordinate of the center of the diamond.
        """
        return len(self._squares) // 2

    def count_squares(self) -> int:
        """
        Return the number of squares in the aztec diamond.
        """
        size = self._size
        double_size = size * 2
        return double_size * double_size - (size * (size-1) // 2)

    def count_tiles(self) -> int:
        """
        Return the number of tiles in the aztec diamond.
        """
        return self.count_squares() // 2

    def full_range(self):
        """
        Return an iterator for the coordinates of tiles.
        """
        return range(self._origin, self._origin + self._size * 2)

    def partial_range(self, x_or_y: int):
        """
        Return an iterator for the sub-range of valid squares coordinates of tiles.
        """
        size = self._size
        double_size = size * 2
        x_or_y -= self._origin
        if x_or_y < size:
            skip = size - (x_or_y + 1)
        else:
            skip = x_or_y - size
        return range(self._origin + skip, self._origin + double_size - skip)

    def tiles(self) -> list:
        """
        Return all half-tiles of the aztec diamond.
        """
        return self._squares

    def increase_size(self):
        """
        Increase the logical size of diamond and move the origin.
        """
        self._size += 1
        self._origin -= 1
        if self._origin < 2:
            self._allocate_tiles(len(self._squares) * 2)
        self.reactor.increase_size(self, self._size)

    def remove_collisions(self):
        """
        Find and remove the tiles about to collide.
        """
        tiles = self._squares
        for y in self.full_range():
            for x in self.partial_range(y):
                tile = tiles[x][y]
                if not tile:
                    continue
                other_x, other_y = tile.move_position(x, y)
                other_tile = tiles[other_x][other_y]
                if not other_tile:
                    continue
                if tile.is_opposite(other_tile):
                    self.reactor.collision(self, x, y)
                    self.reactor.collision(self, other_x, other_y)
                    tiles[x][y] = None
                    tiles[other_x][other_y] = None

    def move_tiles(self):
        """
        Move the tiles in their desired direction.
        """
        dest_tiles = self._tmp_squares
        for y in self.full_range():
            for x in self.partial_range(y):
                dest_tiles[x][y] = None

        tiles = self._squares
        for y in self.full_range():
            for x in self.partial_range(y):
                tile = tiles[x][y]
                if not tile:
                    continue
                new_x, new_y = tile.move_position(x, y)
                self.reactor.move(self, x, y, new_x, new_y)
                dest_tiles[new_x][new_y] = tile
        self._squares = dest_tiles
        self._tmp_squares = tiles

    def fill_holes(self):
        """
        Fill holes of the diamond with new tiles as specified by the tile generator.
        (A typical tile generator will produce a random sequence of horizontal and vertical.)
        """
        tiles = self._squares
        for y in self.full_range():
            for x in self.partial_range(y):
                if tiles[x][y] or tiles[x+1][y] or tiles[x][y+1] or tiles[x+1][y+1]:
                    continue
                is_horizontal = self.tile_generator.is_next_horizontal()
                tile_to_place = available_tiles[is_horizontal]
                for t in tile_to_place:
                    new_x = x + t.placement[0]
                    new_y = y + t.placement[1]
                    tiles[new_x][new_y] = t
                    self.reactor.fill(self, new_x, new_y, t)

    def _noop(self):
        """
        Used to nullify other operations wehn debuggging.
        """
        pass


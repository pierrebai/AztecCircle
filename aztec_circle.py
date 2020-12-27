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
        self._half_tile = {}
        self.tile_generator = tile_generator
        self.reactor = react
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
        """
        Grow the aztec diamond size by one.
        """
        self.reactor.start_grow(self)
        self._increase_size()
        self._remove_collisions()
        self._move_tiles()
        self._fill_holes()
        self.reactor.end_grow(self)

    def size(self) -> int:
        """
        Return the size of the aztec diamond.
        """
        return self._size

    def tiles(self) -> dict:
        """
        Return all half-tiles of the aztec diamond.
        """
        return self._half_tile

    @staticmethod
    def is_corner(x: int, y: int, size: int) -> bool:
        """
        Return if a position is in the excluded corner of the diamond.
        """
        if x >= size:
            x = (size * 2 - 1) - x
        if y >= size:
            y = (size * 2 - 1) - y
        return x + y < size - 1

    def _increase_size(self):
        """
        Increase the logical size of diamond and recenter the tiles.
        """
        self._size += 1
        if self._half_tile:
            new_tiles = {}
            for pos, tile in self._half_tile.items():
                new_tiles[(pos[0]+1, pos[1]+1)] = tile
            self._half_tile = new_tiles
        self.reactor.increase_size(self, self._size)

    def _remove_collisions(self):
        """
        Remove the tiles about to collide.
        """
        new_tiles = self._half_tile.copy()
        for pos, tile in self._half_tile.items():
            other_pos = tile.move(pos)
            if other_pos not in new_tiles:
                continue
            other_tile = new_tiles[other_pos]
            if tile.is_opposite(other_tile):
                self.reactor.collision(self, pos, other_pos)
                del new_tiles[pos]
                del new_tiles[other_pos]
        self._half_tile = new_tiles

    def _move_tiles(self):
        """
        Move the tiles in their desired direction.
        """
        new_tiles = {}
        for pos, tile in self._half_tile.items():
            new_pos = tile.move(pos)
            self.reactor.move(self, pos, new_pos)
            new_tiles[new_pos] = tile
        self._half_tile = new_tiles

    def _is_hole(self, x: int, y: int) -> bool:
        """
        Verify if a given position is the top-left corner of a hole.
        """
        if aztec.is_corner(x, y, self._size):
            return False
        if aztec.is_corner(x+1, y+1, self._size):
            return False
        if (x,y) in self._half_tile:
            return False
        if (x+1,y) in self._half_tile:
            return False
        if (x,y+1) in self._half_tile:
            return False
        if (x+1,y+1) in self._half_tile:
            return False
        return True

    def _fill_holes(self):
        """
        Fill holes of the diamond with new tiles as specified by the tile generator.
        (A typical tile generator will produce a random sequence of horizontal and vertical.)
        """
        double_size = self._size * 2
        for x in range(0, double_size - 1):
            for y in range(0, double_size - 1):
                if not self._is_hole(x, y):
                    continue
                is_horizontal = self.tile_generator.next()
                tile_to_place = available_tiles[is_horizontal]
                for t in tile_to_place:
                    pos = (x + t.placement[0], y + t.placement[1])
                    self._half_tile[pos] = t
                    self.reactor.fill(self, pos, t)

    def _noop(self):
        """
        Used to nullify other operations wehn debuggging.
        """
        pass


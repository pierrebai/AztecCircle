class half_tile:
    #                            vertical            horizontal
    #                          down      up         down      up
    _tile_to_movements  = [ [ (-1, 0), (1, 0) ], [ (0, -1), (0, 1) ] ]

    #                                         vertical                                 horizontal
    #                                down                 up                     down                 up
    #                            1st     2nd         1st     2nd             1st     2nd         1st     2nd
    _tile_to_placements = [ [ [ (0, 1), (0, 0) ], [ (1, 1), (1, 0) ] ], [ [ (1, 0), (0, 0) ], [ (1, 1), (0, 1) ] ] ]

    def __init__(self, is_horizontal: bool, is_positive: bool, is_first_part, is_frozen: bool = False):
        self.is_horizontal = is_horizontal
        self.is_positive   = is_positive
        self.is_first_part = is_first_part
        self.is_frozen     = is_frozen

    def copy(self):
        return half_tile(self.is_horizontal, self.is_positive, self.is_first_part, self.is_frozen)

    def move_position(self, x: int, y: int) -> tuple:
        """
        Move a position in the desired direction of the tile.
        """
        dx, dy = half_tile._tile_to_movements[self.is_horizontal][self.is_positive]
        return (x + dx, y + dy)

    def hole_placement(self) -> tuple:
        """
        Return the placement of this half-tile in the 2x2 hole.
        """
        return half_tile._tile_to_placements[self.is_horizontal][self.is_positive][self.is_first_part]

    def is_opposite(self, other) -> bool:
        """
        Verify if the other tile is moving in the opposite direction.
        That is, if the tile would collide if next to each other in the correct positions.
        """
        return self.is_positive != other.is_positive and self.is_horizontal == other.is_horizontal

    def is_same_type(self, other) -> bool:
        """
        Verify if the tile is of the same type as the other.
        """
        return self.is_positive == other.is_positive and self.is_horizontal == other.is_horizontal

    def is_half(self, other) -> bool:
        """
        Verify if the tile is the opposite half of the other.
        Beware: it is possible to have two opposite next to each other
                and not be the same tile. The relative position (horizontal
                or vertical) of the tiles must be taken into consideration.
        """
        return self.is_positive == other.is_positive and self.is_horizontal == other.is_horizontal and self.is_first_part == True and other.is_first_part == False

    def draw(self):
        """
        To be overridden by code that want to draw tiles.
        """
        pass
    

up_horiz_left    = half_tile(True, True, True)
up_horiz_right   = half_tile(True, True, False)

down_horiz_left  = half_tile(True, False, True)
down_horiz_right = half_tile(True, False, False)

up_verti_left    = half_tile(False, True, True)
up_verti_right   = half_tile(False, True, False)

down_verti_left  = half_tile(False, False, True)
down_verti_right = half_tile(False, False, False)

horiz_tiles = [up_horiz_left, up_horiz_right, down_horiz_left, down_horiz_right]
verti_tiles = [up_verti_left, up_verti_right, down_verti_left, down_verti_right]
available_tiles = [verti_tiles, horiz_tiles]


from reactor import reactor

def separator_type(tiles: dict, pos1: tuple, pos2: tuple, horiz_sep: bool) -> int:
    """
    Determine the type of separation between two adjacent positionin the tiling.
    
    0: empty-to-empty separator
    1: empty-to-tile separator
    2: tile-to-tile separator
    3: linked half-tiles separator
    """
    if pos1 in tiles and pos2 in tiles:
        return [2, 3][tiles[pos1].is_horizontal == horiz_sep and tiles[pos1].is_half(tiles[pos2])]
    else:
        return [0, 1][pos1 in tiles or pos2 in tiles]

def draw_inter_horizontal(tiles: dict, pos1: tuple, pos2: tuple, line: list):
    """
    Add the inter-column separator between two tiles on the same row.
    """
    line.append([' ', '|', '|', ' '][separator_type(tiles, pos1, pos2, True)])

def draw_inter_horizontal_for_vertical(tiles: dict, x: int, y: int, line: list):
    """
    Add the inter-column separator in the inter-row separator line.
    """
    horiz_seps = (separator_type(tiles, (x-1, y  ), (x  , y  ), True),
                  separator_type(tiles, (x-1, y+1), (x  , y+1), True))
    verti_seps = (separator_type(tiles, (x-1, y  ), (x-1, y+1), False),
                  separator_type(tiles, (x  , y  ), (x  , y+1), False))
    if all(map(lambda s: s == 3, verti_seps)):
        line.append('|')
    elif any(map(lambda s: s == 3, verti_seps)) and any(map(lambda s: s == 0, verti_seps)):
        line.append('|')
    elif all(map(lambda s: s == 3, horiz_seps)):
        line.append('-')
    elif any(map(lambda s: s == 3, horiz_seps)) and any(map(lambda s: s == 0, horiz_seps)):
        line.append('-')
    elif all(map(lambda s: s == 0, horiz_seps)) and all(map(lambda s: s == 0, verti_seps)):
        line.append(' ')
    else:
        line.append('+')

def draw_inter_verticals(az, tiles: dict, y: int):
    """
    Add the inter-row separator line.
    """
    line = []
    for x in az.coord_range():
        draw_inter_horizontal_for_vertical(tiles, x, y, line)
        draw_inter_vertical(tiles, (x, y), (x, y+1), line)
    draw_inter_horizontal_for_vertical(tiles, x+1, y, line)
    print(''.join(line))

def draw_inter_vertical(tiles: dict, pos1: tuple, pos2: tuple, line):
    """
    Add one part of the inter-row separator line for a single column.
    """
    line.append(['   ', '---', '---', '   '][separator_type(tiles, pos1, pos2, False)])

def draw_aztec_ascii(az):
    """
    Draw the aztec tiling in ASCII.
    """
    tile_colors = [ ['Y', 'R'], ['B', 'G'] ]
    tiles = az.tiles()
    for y in az.coord_range():
        draw_inter_verticals(az, tiles, y-1)
        line = []
        for x in az.coord_range():
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
    draw_inter_verticals(az, tiles, y)


class draw_ascii_reactor(reactor):
    """
    Draw the aztec tiling in ASCII at the end of each growth.
    """

    def end_grow(self, az):
        draw_aztec_ascii(az)

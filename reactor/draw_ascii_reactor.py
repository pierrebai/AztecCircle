from .reactor import reactor

def separator_type(tiles: list, x1: int, y1: int, x2: int, y2: int, horiz_sep: bool) -> int:
    """
    Determine the type of separation between two adjacent positionin the tiling.

    0: empty-to-empty separator
    1: empty-to-tile separator
    2: tile-to-tile separator
    3: linked half-tiles separator
    """
    t1 = tiles[x1][y1]
    t2 = tiles[x2][y2]
    if t1 and t2:
        return [2, 3][t1.is_horizontal == horiz_sep and t1.is_half(t2)]
    else:
        return [0, 1][bool(t1) or bool(t2)]

def draw_inter_horizontal(tiles: list, x1: int, y1: int, x2: int, y2: int, line: list):
    """
    Add the inter-column separator between two tiles on the same row.
    """
    line.append([' ', '|', '|', ' '][separator_type(tiles, x1, y2, x2, y2, True)])

def draw_inter_horizontal_for_vertical(tiles: list, x: int, y: int, line: list):
    """
    Add the inter-column separator in the inter-row separator line.
    """
    horiz_seps = (separator_type(tiles, x-1, y  , x  , y  , True),
                  separator_type(tiles, x-1, y+1, x  , y+1, True))
    verti_seps = (separator_type(tiles, x-1, y  , x-1, y+1, False),
                  separator_type(tiles, x  , y  , x  , y+1, False))
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

def draw_inter_verticals(az, tiles: list, y: int):
    """
    Add the inter-row separator line.
    """
    line = []
    for x in az.full_range():
        draw_inter_horizontal_for_vertical(tiles, x, y, line)
        draw_inter_vertical(tiles, x, y, x, y+1, line)
    draw_inter_horizontal_for_vertical(tiles, x+1, y, line)
    print(''.join(line))

def draw_inter_vertical(tiles: list, x1: int, y1: int, x2: int, y2: int, line):
    """
    Add one part of the inter-row separator line for a single column.
    """
    line.append(['   ', '---', '---', '   '][separator_type(tiles, x1, y1, x2, y2, False)])

def draw_aztec_ascii(az):
    """
    Draw the aztec tiling in ASCII.
    """
    tile_colors = [ ['Y', 'R'], ['B', 'G'] ]
    tiles = az.tiles()
    for y in az.full_range():
        draw_inter_verticals(az, tiles, y-1)
        line = []
        for x in az.full_range():
            draw_inter_horizontal(tiles, x-1, y, x, y, line)
            tile = tiles[x][y]
            if not tile:
                line.append('   ')
            else:
                color = tile_colors[tile.is_horizontal][tile.is_positive]
                line.append(f' {color} ')
        draw_inter_horizontal(tiles, x, y, x+1, y, line)
        print(''.join(line))
    draw_inter_verticals(az, tiles, y)


class draw_ascii_reactor(reactor):
    """
    Draw the aztec tiling in ASCII at the end of each growth.
    """

    def fills_done(self, az):
        draw_aztec_ascii(az)


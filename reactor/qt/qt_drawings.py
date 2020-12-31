from PyQt5.QtGui import QBrush, QColor, QPen, QPolygonF, QPainter
from PyQt5.QtCore import QRectF, QPointF, QLineF, Qt


class qt_drawings:
    """
    Qt data used to draw tiles.
    """

    tile_size = 10

    tile_colors = [ QColor(235, 180, 40), QColor(255, 84, 46), QColor(68, 125, 255), QColor(83, 223, 56) ]
    tile_brushes = [ [QBrush(tile_colors[0]), QBrush(tile_colors[1])], [QBrush(tile_colors[2]), QBrush(tile_colors[3])] ]

    no_color = QColor(0, 0, 0, 0)
    no_pen = QPen(no_color)
    no_pen.setWidth(0)
    no_brush = QBrush(no_color)

    black_color = QColor(0, 0, 0)
    black_pen = QPen(black_color)
    black_brush = QBrush(black_color)

    cyan_color = QColor(30, 190, 220)
    cyan_brush = QBrush(cyan_color)

    gray_color = QColor(220, 220, 220, 80)
    gray_pen = QPen(gray_color)
    gray_brush = QBrush(gray_color)

    red_color = QColor(255, 40, 40)
    red_brush = QBrush(red_color)
    red_pen = QPen(red_color.darker(130))

    cross_polygon = QPolygonF([
         QPointF(1, 3), QPointF(3, 1), QPointF(tile_size / 2, 3),
         QPointF(tile_size - 3, 1), QPointF(tile_size - 1, 3), QPointF(tile_size - 3, tile_size / 2),
         QPointF(tile_size - 1, tile_size - 3), QPointF(tile_size - 3, tile_size - 1), QPointF(tile_size / 2, tile_size - 3),
         QPointF(3, tile_size - 1), QPointF(1, tile_size - 3), QPointF(3, tile_size / 2),
    ])

    arrow_polygon = QPolygonF([
        QPointF(2, 5), QPointF(tile_size / 2, 1), QPointF(tile_size - 2, 5),
        QPointF(tile_size / 2 + 1, 4), QPointF(tile_size / 2 + 1, tile_size - 1),
        QPointF(tile_size / 2 - 1, tile_size - 1), QPointF(tile_size / 2 - 1, 4), 
    ])

    @staticmethod
    def tile_to_brush(tile) -> QBrush:
        return qt_drawings.tile_brushes[tile.is_horizontal][tile.is_positive]

    @staticmethod
    def paint_tile(painter: QPainter, wx: int, wy: int, tile, tile_size: int):
        width  = 2 * tile_size if tile.is_horizontal else tile_size
        height = tile_size if tile.is_horizontal else 2 * tile_size
        painter.fillRect(wx, wy, width, height, qt_drawings.tile_to_brush(tile))

        if tile_size > 5:
            painter.drawRect(wx, wy, width, height)



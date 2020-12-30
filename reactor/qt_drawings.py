from .reactor import reactor

from PyQt5.QtGui import QBrush, QColor, QPen, QPolygonF, QPainter
from PyQt5.QtCore import QRectF, QPointF, QLineF, Qt


class qt_drawings:
    """
    Qt data used to draw tiles.
    """

    tile_size = 10

    tile_colors = [ QColor(235, 180, 40), QColor(255, 84, 46), QColor(68, 125, 255), QColor(83, 223, 56) ]
    tile_brushes = [ [QBrush(tile_colors[0]), QBrush(tile_colors[1])], [QBrush(tile_colors[2]), QBrush(tile_colors[3])] ]

    black_pen = QPen(QColor(0, 0, 0))
    gray_pen = QPen(QColor(180, 180, 180, 180))

    red_color = QColor(255, 40, 40)
    red_brush = QBrush(red_color)
    red_pen = QPen(red_color)
    cross_delta_1 = 3
    cross_delta_2 = 1
    cross_polygon = QPolygonF([
         QPointF(cross_delta_2, cross_delta_1), QPointF(cross_delta_1, cross_delta_2), QPointF(tile_size / 2, cross_delta_1),
         QPointF(tile_size - cross_delta_1, cross_delta_2), QPointF(tile_size - cross_delta_2, cross_delta_1), QPointF(tile_size - cross_delta_1, tile_size / 2),
         QPointF(tile_size - cross_delta_2, tile_size - cross_delta_1), QPointF(tile_size - cross_delta_1, tile_size - cross_delta_2), QPointF(tile_size / 2, tile_size - cross_delta_1),
         QPointF(cross_delta_1, tile_size - cross_delta_2), QPointF(cross_delta_2, tile_size - cross_delta_1), QPointF(cross_delta_1, tile_size / 2),
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



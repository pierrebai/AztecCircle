from aztec_circle import aztec
from reactor import reactor

from PyQt5.QtGui import QBrush, QColor, QPen, QPolygonF, QPainter
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QMarginsF, QRectF, QPointF, QLineF, Qt


class aztec_canvas(QWidget):
    """
    A Qt widget that can draw the tiles of an aztec diamond.
    """

    tile_colors = [ QColor(235, 180, 40), QColor(255, 84, 46), QColor(68, 125, 255), QColor(83, 223, 56) ]
    tile_pens = [ [QPen(tile_colors[0].darker(120)), QPen(tile_colors[1].darker(120))], [QPen(tile_colors[2].darker(120)), QPen(tile_colors[3].darker(120))] ]
    tile_brushes = [ [QBrush(tile_colors[0]), QBrush(tile_colors[1])], [QBrush(tile_colors[2]), QBrush(tile_colors[3])] ]

    black_pen = QPen(QColor(0, 0, 0))

    tile_border_points = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0), (1, 0), (1, 1), (0, 1)]
    tile_border_ranges = [[(3, 6), (1, 4)], [(2, 5), (0, 3)]]

    @staticmethod
    def tile_to_brush(tile) -> QBrush:
        return aztec_canvas.tile_brushes[tile.is_horizontal][tile.is_positive]

    @staticmethod
    def tile_to_pen(tile) -> QPen:
        return aztec_canvas.tile_pens[tile.is_horizontal][tile.is_positive]

    def __init__(self, *args, **kwargs):
        super(aztec_canvas, self).__init__(*args, **kwargs)
        self.tile_size = 10
        self.az = None

    def paintEvent(self, event):
        az = self.az
        if not az:
            return super(aztec_canvas, self).paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        tiles = az.tiles()

        tile_size = self.tile_size
        start_x = (self.rect().width()  - tile_size * az.size() * 2) / 2
        start_y = (self.rect().height() - tile_size * az.size() * 2) / 2

        wy = start_y
        for y in az.full_range():
            wx = start_x
            for x in az.full_range():
                tile = tiles[x][y]
                if tile:
                    self.paint_tile(painter, wx, wy, tile, tile_size)
                wx += tile_size
            wy += tile_size

        # Faster rectangle drawing by accumulating them.
        # But... would need to optimize line drawing too
        # for this to be worthwhile...

        # def flush_rect(previous_brush, rx):
        #     if not previous_brush:
        #         return
        #     painter.fillRect(rx, wy, wx - rx, tile_size, previous_brush)

        # wy = start_y
        # for y in az.full_range():
        #     wx = start_x
        #     rx = None
        #     previous_brush = None
        #     for x in az.full_range():
        #         tile = tiles[x][y]
        #         new_brush = aztec_canvas.tile_to_brush(tile) if tile else None
        #         if new_brush != previous_brush:
        #             flush_rect(previous_brush, rx)
        #             rx = wx
        #             previous_brush = new_brush
        #         wx += tile_size
        #     flush_rect(previous_brush, rx)
        #     wy += tile_size

    def adjust_view_to_fit(self, az, size: int):
        w = self.rect().width()
        h = self.rect().height()
        self.tile_size = min(40, min(w, h) // ((size + 1) * 2))
        aztec_canvas.black_pen = QPen(QColor(0, 0, 0), max(1, self.tile_size / 10))

    def paint_tile(self, painter: QPainter, wx: int, wy: int, tile, tile_size: int):
        painter.fillRect(wx, wy, tile_size, tile_size, aztec_canvas.tile_to_brush(tile))

        if tile_size > 5:
            painter.setPen(aztec_canvas.black_pen)
            start, end = aztec_canvas.tile_border_ranges[tile.is_horizontal][tile.is_high_part]
            for i in range(start, end):
                x1 = wx + aztec_canvas.tile_border_points[i  ][0] * tile_size
                y1 = wy + aztec_canvas.tile_border_points[i  ][1] * tile_size
                x2 = wx + aztec_canvas.tile_border_points[i+1][0] * tile_size
                y2 = wy + aztec_canvas.tile_border_points[i+1][1] * tile_size
                painter.drawLine(x1, y1, x2, y2)


class canvas_reactor(reactor):
    def __init__(self):
        self.canvas = aztec_canvas()
        self.center = 0
        self.reset()

    def widget(self):
        return self.canvas

    def reset(self):
        pass

    def reallocate(self, az: aztec, old_amount: int, new_amount: int):
        self.center = new_amount // 2
        self.canvas.az = az

    def increase_size(self, az, size):
        self.canvas.adjust_view_to_fit(az, size)

    def collisions_done(self, az):
        self.canvas.update()

    def moves_done(self, az):
        self.canvas.update()

    def fills_done(self, az):
        self.canvas.update()



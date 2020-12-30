from .reactor import reactor
from .qt_drawings import qt_drawings

from PyQt5.QtGui import QBrush, QColor, QPen, QPolygonF, QPainter
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QMarginsF, QRectF, QPointF, QLineF, Qt


class aztec_canvas(QWidget, qt_drawings):
    """
    A Qt widget that can draw the tiles of an aztec diamond.
    """

    def __init__(self, *args, **kwargs):
        super(aztec_canvas, self).__init__(*args, **kwargs)
        self.tile_size = 10
        self.az = None

    def adjust_view_to_fit(self, az, size: int):
        w = self.rect().width()
        h = self.rect().height()
        self.tile_size = min(40, min(w, h) // ((size + 1) * 2))
        qt_drawings.black_pen = QPen(QColor(0, 0, 0), max(1, self.tile_size / 10))

    def paintEvent(self, event):
        az = self.az
        if not az:
            return super(aztec_canvas, self).paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        painter.setPen(qt_drawings.black_pen)

        tiles = az.tiles()

        tile_size = self.tile_size
        start_x = (self.rect().width()  - tile_size * az.size() * 2) / 2
        start_y = (self.rect().height() - tile_size * az.size() * 2) / 2

        wy = start_y
        for y in az.full_range():
            wx = start_x
            for x in az.full_range():
                tile = tiles[x][y]
                if tile and tile.is_first_part:
                    qt_drawings.paint_tile(painter, wx, wy, tile, tile_size)
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
        #         if tile.is_first_part:
        #             new_brush = qt_drawings.tile_to_brush(tile) if tile else None
        #             if new_brush != previous_brush:
        #                 flush_rect(previous_brush, rx)
        #                 rx = wx
        #                 previous_brush = new_brush
        #         wx += tile_size
        #     flush_rect(previous_brush, rx)
        #     wy += tile_size


class canvas_reactor(reactor):
    def __init__(self):
        self.canvas = aztec_canvas()
        self.center = 0
        self.reset()

    def widget(self):
        return self.canvas

    def reset(self):
        pass

    def reallocate(self, az, old_amount: int, new_amount: int):
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



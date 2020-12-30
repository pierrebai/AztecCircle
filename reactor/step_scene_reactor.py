from .base_scene_reactor import base_scene_reactor
from aztec_circle import aztec

from PyQt5.QtGui import QBrush, QColor, QPen, QPolygonF
from PyQt5.QtWidgets import QGraphicsPolygonItem
from PyQt5.QtCore import QRectF, QPointF, QLineF, Qt

class step_scene_reactor(base_scene_reactor):

    def __init__(self, show_boundary = False, *args, **kwargs):
        super(step_scene_reactor, self).__init__(*args, **kwargs)
        self.center = 0
        self.show_boundary = show_boundary
        self.reset()

    def reset(self):
        super(step_scene_reactor, self).reset()
        self.items = []
        self.new_items = []
        self.boundary = None

    def reallocate(self, az, old_amount: int, new_amount: int):
        skip, self.items, self.new_items = aztec.reallocate_data(old_amount, new_amount, self.items, self.new_items)
        self.center = new_amount // 2

    def increase_size(self, az, size):
        if self.show_boundary:
            coord = -qt_drawings.tile_size * (self.center + size)
            width = qt_drawings.tile_size * size * 2
            if not self.boundary:
                self.boundary = self.scene.addRect(coord, coord, width, width, qt_drawings.black_pen)
            else:
                self.boundary.setRect(coord, coord, width, width)
        self.adjust_view_to_fit()

    def collision(self, az, x, y):
        for item in self.items[x][y]:
            self.scene.removeItem(item)

    def move(self, az, x1, y1, x2, y2):
        center = self.center
        items = self.items[x1][y1]
        for item in items:
            item.setPos(*self.pos_to_scene(x2 - center, y2 - center))
        self.new_items[x2][y2] = items

    def fill(self, az, x, y, tile):
        center = self.center
        items = self.create_scene_tile(x - center, y - center, tile)
        self.new_items[x][y] = items

    def fills_done(self, az):
        self.items, self.new_items = self.new_items, self.items
        self.adjust_view_to_fit()


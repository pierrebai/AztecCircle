from base_scene_reactor import base_scene_reactor, tile_size

from PyQt5.QtGui import QBrush, QColor, QPen, QPolygonF
from PyQt5.QtWidgets import QGraphicsPolygonItem
from PyQt5.QtCore import QRectF, QPointF, QLineF, Qt

class step_scene_reactor(base_scene_reactor):
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

    def __init__(self, *args, **kwargs):
        super(step_scene_reactor, self).__init__(*args, **kwargs)
        self.show_collisions = True
        self.reset()

    def reset(self):
        super(step_scene_reactor, self).reset()
        self.items = {}
        self.new_items = {}

    def start_grow(self, az):
        self.new_items = {}

    def increase_size(self, az, size):
        self.adjust_view_to_fit()

    def collision_found(self, az, pos):
        if not self.show_collisions:
            return
        scene_pos = self.pos_to_scene(pos)
        item = QGraphicsPolygonItem(step_scene_reactor.cross_polygon)
        item.setPos(*scene_pos)
        item.setBrush(step_scene_reactor.red_brush)
        item.setPen(step_scene_reactor.red_pen)
        self.items[pos].append(item)
        self.scene.addItem(item)

    def collision_removed(self, az, pos):
        for item in self.items[pos]:
            self.scene.removeItem(item)

    def move(self, az, pos1, pos2):
        items = self.items[pos1]
        for item in items:
            item.setPos(*self.pos_to_scene(pos2))
        self.new_items[pos2] = items

    def fill(self, az, pos, tile):
        items = self.create_scene_tile(pos, tile)
        self.new_items[pos] = items

    def end_grow(self, az):
        self.items = self.new_items
        self.new_items = {}
        self.adjust_view_to_fit()


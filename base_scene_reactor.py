from reactor import reactor

from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsItem, QGraphicsRectItem

class base_scene_reactor(reactor):
    tile_colors = [ QColor(235, 180, 40), QColor(255, 84, 46), QColor(68, 125, 255), QColor(83, 223, 56) ]
    tile_pens = [ [QPen(tile_colors[0].darker(120)), QPen(tile_colors[1].darker(120))], [QPen(tile_colors[2].darker(120)), QPen(tile_colors[3].darker(120))] ]
    tile_brushes = [ [QBrush(tile_colors[0]), QBrush(tile_colors[1])], [QBrush(tile_colors[2]), QBrush(tile_colors[3])] ]

    def __init__(self, scene: QGraphicsScene, view: QGraphicsView):
        self.scene = scene
        self.view = view
        self.tile_size = 10

    def start_grow(self, az):
        vs = self.view.size()
        usable = min(vs.width(), vs.height())
        self.tile_size = usable // ((az.size() + 1) * 2)

    def create_scene_tile(self, pos: tuple, tile) -> QGraphicsItem:
        item = QGraphicsRectItem(*self.pos_to_scene(pos), self.tile_size, self.tile_size)
        item.setBrush(base_scene_reactor.tile_to_brush(tile))
        item.setPen(base_scene_reactor.tile_to_pen(tile))
        self.scene.addItem(item)
        return item

    def pos_to_scene(self, pos: tuple) -> tuple:
        ts = self.tile_size
        return (pos[0] * ts, pos[1] * ts)

    @staticmethod
    def tile_to_brush(tile) -> QBrush:
        return base_scene_reactor.tile_brushes[tile.is_horizontal][tile.is_positive]

    @staticmethod
    def tile_to_pen(tile) -> QPen:
        return base_scene_reactor.tile_pens[tile.is_horizontal][tile.is_positive]


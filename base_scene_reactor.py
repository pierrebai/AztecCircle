from reactor import reactor

from PyQt5.QtGui import QBrush, QColor, QPen, QPolygonF
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsItem, QGraphicsRectItem, QGraphicsPolygonItem, QGraphicsLineItem
from PyQt5.QtCore import QMarginsF, QRectF, QPointF, QLineF, Qt


tile_size = 10
class base_scene_reactor(reactor):
    tile_colors = [ QColor(235, 180, 40), QColor(255, 84, 46), QColor(68, 125, 255), QColor(83, 223, 56) ]
    tile_pens = [ [QPen(tile_colors[0].darker(120)), QPen(tile_colors[1].darker(120))], [QPen(tile_colors[2].darker(120)), QPen(tile_colors[3].darker(120))] ]
    tile_brushes = [ [QBrush(tile_colors[0]), QBrush(tile_colors[1])], [QBrush(tile_colors[2]), QBrush(tile_colors[3])] ]

    black_pen = QPen(QColor(0, 0, 0))

    points = [QPointF(0, 0), QPointF(tile_size, 0), QPointF(tile_size, tile_size), QPointF(0, tile_size), QPointF(0, 0), QPointF(tile_size, 0), QPointF(tile_size, tile_size), QPointF(0, tile_size)]
    ranges = [[(3, 6), (1, 4)], [(2, 5), (0, 3)]]

    def __init__(self, scene: QGraphicsScene, view: QGraphicsView):
        self.scene = scene
        self.view = view

    def create_scene_tile(self, pos: tuple, tile) -> QGraphicsItem:
        items = []

        scene_pos = self.pos_to_scene(pos)

        item = QGraphicsRectItem(0, 0, tile_size, tile_size)
        item.setPos(*scene_pos)
        item.setBrush(base_scene_reactor.tile_to_brush(tile))
        item.setPen(base_scene_reactor.tile_to_pen(tile))
        items.append(item)

        start, end = base_scene_reactor.ranges[tile.is_horizontal][tile.is_high_part]
        for i in range(start, end):
            item = QGraphicsLineItem(QLineF(base_scene_reactor.points[i], base_scene_reactor.points[i+1]))
            item.setPos(*scene_pos)
            item.setPen(base_scene_reactor.black_pen)
            items.append(item)

        for item in items:
            self.scene.addItem(item)

        return items

    def adjust_view_to_fit(self):
        self.scene.update()
        viewOrigin = self.view.rect().topLeft()
        sceneOrigin = self.view.mapFromScene(self.scene.sceneRect().translated(-15, -15).topLeft())
        if viewOrigin.x() >= sceneOrigin.x() or viewOrigin.y() >= sceneOrigin.y():
            self.view.fitInView(QRectF(0, 0, 200, 200).united(self.scene.sceneRect().marginsAdded(QMarginsF(100, 100, 100, 100))), Qt.KeepAspectRatio)

    def pos_to_scene(self, pos: tuple) -> tuple:
        return (pos[0] * tile_size, pos[1] * tile_size)

    @staticmethod
    def tile_to_brush(tile) -> QBrush:
        return base_scene_reactor.tile_brushes[tile.is_horizontal][tile.is_positive]

    @staticmethod
    def tile_to_pen(tile) -> QPen:
        return base_scene_reactor.tile_pens[tile.is_horizontal][tile.is_positive]


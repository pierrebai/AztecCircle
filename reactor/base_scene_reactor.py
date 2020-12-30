from .reactor import reactor
from .qt_drawings import qt_drawings

from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsItem, QGraphicsRectItem, QGraphicsPolygonItem, QGraphicsLineItem
from PyQt5.QtCore import QMarginsF, QRectF, Qt


class base_scene_reactor(reactor, qt_drawings):

    def __init__(self):
        self.scene = QGraphicsScene()

        self.view = QGraphicsView(self.scene)
        self.view.setInteractive(False)
        self.view.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

    def widget(self):
        return self.view

    def reallocate_scene(self):
        self.scene = QGraphicsScene()

        self.view.setScene(self.scene)
        self.view.resetTransform()
        self.view.resetCachedContent()
        self.view.setSceneRect(QRectF())

        self.view.fitInView(self.scene.sceneRect().marginsAdded(QMarginsF(10, 10, 10, 10)), Qt.KeepAspectRatio)
        
    def reset(self):
        self.reallocate_scene()

    def create_scene_tile(self, x: int, y: int, tile) -> QGraphicsItem:
        items = []

        x, y = self.pos_to_scene(x, y)

        width  = 2 * qt_drawings.tile_size if tile.is_horizontal else qt_drawings.tile_size
        height = qt_drawings.tile_size if tile.is_horizontal else 2 * qt_drawings.tile_size
        item = QGraphicsRectItem(0, 0, width, height)
        item.setPos(x, y)
        item.setBrush(qt_drawings.tile_to_brush(tile))
        item.setPen(qt_drawings.black_pen)
        items.append(item)

        for item in items:
            self.scene.addItem(item)

        return items

    def adjust_view_to_fit(self):
        viewOrigin = self.view.rect().topLeft()
        sceneOrigin = self.view.mapFromScene(self.scene.sceneRect().translated(-15, -15).topLeft())
        if viewOrigin.x() >= sceneOrigin.x() or viewOrigin.y() >= sceneOrigin.y():
            #self.view.fitInView(QRectF(0, 0, 50, 50).united(self.scene.sceneRect().marginsAdded(QMarginsF(100, 100, 100, 100))), Qt.KeepAspectRatio)
            self.view.fitInView(self.scene.sceneRect().marginsAdded(QMarginsF(50, 50, 50, 50)), Qt.KeepAspectRatio)

    def pos_to_scene(self, x: int, y: int) -> tuple:
        return (x * qt_drawings.tile_size, y * qt_drawings.tile_size)

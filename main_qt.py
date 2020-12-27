from aztec_circle import aztec
from reactor import reactor
from repeatable_random import repeatable_random

from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import *

import sys

class base_scene_reactor(reactor):
    tile_pens = [ [QPen(QColor(255, 255, 0)), QPen(QColor(255, 0, 0))], [QPen(QColor(0, 0, 255)), QPen(QColor(0, 255, 0))] ]
    tile_brushes = [ [QBrush(QColor(255, 255, 0)), QBrush(QColor(255, 0, 0))], [QBrush(QColor(0, 0, 255)), QBrush(QColor(0, 255, 0))] ]

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
        return scene_reactor.tile_brushes[tile.is_horizontal][tile.is_positive]

    @staticmethod
    def tile_to_pen(tile) -> QPen:
        return scene_reactor.tile_pens[tile.is_horizontal][tile.is_positive]


class scene_reactor(base_scene_reactor):
    def __init__(self, *args, **kwargs):
        super(simple_scene_reactor, self).__init__(*args, **kwargs)
        self.items = {}
        self.new_items = {}

    def start_grow(self, az):
        self.new_items = {}

    def increase_size(self, az, size):
        # TODO: make reactor more general to avoid to have to replicate the aztec actions here.
        new_items = {}
        for pos, item in self.items.items():
            new_items[(pos[0]+1, pos[1]+1)] = item
        self.items = new_items

    def collision(self, az, pos1, pos2):
        self.scene.removeItem(self.items[pos1])
        self.scene.removeItem(self.items[pos2])
        #self.scene.update()

    def move(self, az, pos1, pos2):
        item = self.items[pos1]
        item.setPos(*self.pos_to_scene(pos2))
        self.new_items[pos2] = item
        #self.scene.update()

    def fill(self, az, pos, tile):
        item = self.create_scene_tile(pos, tile)
        self.new_items[pos] = item
        #self.scene.update()

    def end_grow(self, az):
        self.items = self.new_items
        self.new_items = {}
        self.scene.update()

class simple_scene_reactor(base_scene_reactor):
    def __init__(self, *args, **kwargs):
        super(simple_scene_reactor, self).__init__(*args, **kwargs)
        self.scene = scene

    def end_grow(self, az):
        self.scene.clear()
        for pos, tile in az.tiles().items():
            self.create_scene_tile(pos, tile)
        self.scene.update()


app = QApplication(sys.argv)

scene = QGraphicsScene()
scene_view = QGraphicsView(scene)
#scene_react = scene_reactor(scene, scene_view)
scene_react = simple_scene_reactor(scene, scene_view)

window = QMainWindow()
window.setWindowTitle("Aztec Artic Circle")
window.setCentralWidget(scene_view)
window.show()

seed = 7
az = aztec(0, repeatable_random(seed), scene_react)

timer = QTimer()
timer.setInterval(10)
timer.start()

@timer.timeout.connect
def on_timer():
    az.grow()

app.exec_()


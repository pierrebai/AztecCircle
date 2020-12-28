from base_scene_reactor import base_scene_reactor

from PyQt5.QtWidgets import QGraphicsScene

class simple_scene_reactor(base_scene_reactor):
    def __init__(self, *args, **kwargs):
        super(simple_scene_reactor, self).__init__(*args, **kwargs)
        self.reset()

    def end_grow(self, az):
        self.scene = QGraphicsScene()
        tiles = az.tiles()
        for x in az.full_range():
            for y in az.partial_range(x):
                pos = (x, y)
                tile = tiles[x][y]
                self.create_scene_tile(pos, tile)
        self.view.setScene(self.scene)
        self.adjust_view_to_fit()

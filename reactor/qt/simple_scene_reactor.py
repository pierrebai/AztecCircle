from .base_scene_reactor import base_scene_reactor

from PyQt5.QtWidgets import QGraphicsScene


class simple_scene_reactor(base_scene_reactor):
    """
    Reactor using a Qt graphics scene to show changes after each full growth.
    """

    def __init__(self, *args, **kwargs):
        super(simple_scene_reactor, self).__init__(*args, **kwargs)
        self.reset()

    def fills_done(self, az):
        self.scene = QGraphicsScene()
        tiles = az.tiles()
        for x in az.full_range():
            for y in az.partial_range(x):
                tile = tiles[x][y]
                if tile.is_first_part:
                    self.create_scene_tile(x, y, tile)
        self.view.setScene(self.scene)
        self.adjust_view_to_fit()

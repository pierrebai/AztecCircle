from .base_scene_reactor import base_scene_reactor
from .qt_drawings import qt_drawings
from aztec_circle import aztec


class step_scene_reactor(base_scene_reactor):
    """
    Reactor using a Qt graphics scene to show step-by-step changes.
    """

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

    def increase_size(self, az, origin, size):
        if self.show_boundary:
            coord = qt_drawings.tile_size * (origin - self.center) - 8
            width = qt_drawings.tile_size * size * 2 + 16
            if not self.boundary:
                self.boundary = self.scene.addRect(coord, coord, width, width, qt_drawings.gray_pen)
            else:
                self.boundary.setRect(coord, coord, width, width)
        self.adjust_view_to_fit()

    def collision(self, az, x, y):
        item = self.items[x][y]
        self.scene.removeItem(item)

    def move(self, az, x1, y1, x2, y2):
        center = self.center
        item = self.items[x1][y1]
        item.setPos(*self.pos_to_scene(x2 - center, y2 - center))
        self.new_items[x2][y2] = item

    def fill(self, az, x, y, tile):
        center = self.center
        item = self.create_scene_tile(x - center, y - center, tile)
        self.new_items[x][y] = item

    def fills_done(self, az):
        self.items, self.new_items = self.new_items, self.items
        self.adjust_view_to_fit()


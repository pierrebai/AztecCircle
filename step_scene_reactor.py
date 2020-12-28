from base_scene_reactor import base_scene_reactor

class step_scene_reactor(base_scene_reactor):
    def __init__(self, *args, **kwargs):
        super(step_scene_reactor, self).__init__(*args, **kwargs)
        self.items = {}
        self.new_items = {}

    def reset(self):
        self.items = {}
        self.new_items = {}
        self.scene.clear()
        self.view.fitInView(self.scene.sceneRect())

    def start_grow(self, az):
        self.new_items = {}

    def increase_size(self, az, size):
        self.adjust_view_to_fit()

    def collision(self, az, pos1, pos2):
        self.scene.removeItem(self.items[pos1])
        self.scene.removeItem(self.items[pos2])

    def move(self, az, pos1, pos2):
        item = self.items[pos1]
        item.setPos(*self.pos_to_scene(pos2))
        #item.setRect(*self.pos_to_scene(pos2), self.tile_size, self.tile_size)
        self.new_items[pos2] = item

    def fill(self, az, pos, tile):
        item = self.create_scene_tile(pos, tile)
        self.new_items[pos] = item

    def end_grow(self, az):
        self.items = self.new_items
        self.new_items = {}
        self.adjust_view_to_fit()


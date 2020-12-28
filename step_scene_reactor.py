from base_scene_reactor import base_scene_reactor

class step_scene_reactor(base_scene_reactor):
    def __init__(self, *args, **kwargs):
        super(step_scene_reactor, self).__init__(*args, **kwargs)
        self.reset()

    def reset(self):
        super(step_scene_reactor, self).reset()
        self.items = {}
        self.new_items = {}

    def start_grow(self, az):
        self.new_items = {}

    def increase_size(self, az, size):
        self.adjust_view_to_fit()

    def collision(self, az, pos1, pos2):
        for item in self.items[pos1]:
            self.scene.removeItem(item)
        for item in self.items[pos2]:
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


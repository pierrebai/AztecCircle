from aztec_circle import aztec
from simple_scene_reactor import simple_scene_reactor
from step_scene_reactor import step_scene_reactor
from tile_generator import sequence_tile_generator

class aztec_scene_widget:
    """
    Holds a scene reactor, tile generator and aztec diamond.
    """
    def __init__(self):
        self.scene_react = step_scene_reactor()
        #self.scene_react = simple_scene_reactor()
        self.generator = sequence_tile_generator(7, "r")
        self.step_name = ""
        self.reset()

    def reset(self):
        self.step_state = 0
        self.scene_react.reset()
        self.generator.reset()
        self.az = aztec(1, self.generator, self.scene_react)

    def widget(self):
        return self.az.scene_react.view

    def _increase_size_step(self):
        self.az.reactor.start_grow(self.az)
        self.az.increase_size()

    def _remove_collisions_step(self):
        self.az.remove_collisions()

    def _move_tiles_step(self):
        self.az.move_tiles()

    def _fill_holes_step(self):
        self.az.fill_holes()
        self.az.reactor.end_grow(self.az)

    steps = {
        0: (_increase_size_step, "Grow diamond"),
        1: (_remove_collisions_step, "Remove collisions"),
        2: (_move_tiles_step, "Move tiles"),
        3: (_fill_holes_step, "Fill holes"),
    }

    def step(self):
        func, name = aztec_scene_widget.steps[self.step_state]
        self.step_name = name
        func(self)
        self.step_state = (self.step_state+1) % len(aztec_scene_widget.steps)

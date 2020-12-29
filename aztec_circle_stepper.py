from aztec_circle import aztec
from tile_generator import sequence_tile_generator

class aztec_circle_stepper:
    """
    Holds a aztec diamond and step through its algorithm.
    """
    def __init__(self, reactor):
        self.reactor = reactor
        self.generator = sequence_tile_generator(7, "r")
        self.step_name = ""
        self.reset()

    def reset(self):
        self.step_state = 0
        self.reactor.reset()
        self.generator.reset()
        self.az = aztec(1, self.generator, self.reactor)

    def _increase_size_step(self):
        self.az.increase_size()

    def _remove_collisions_step(self):
        self.az.remove_collisions()

    def _move_tiles_step(self):
        self.az.move_tiles()

    def _fill_holes_step(self):
        self.az.fill_holes()

    steps = {
        0: (_increase_size_step, "Grow diamond"),
        1: (_remove_collisions_step, "Remove collisions"),
        2: (_move_tiles_step, "Move tiles"),
        3: (_fill_holes_step, "Fill holes"),
    }

    def step(self):
        func, name = aztec_circle_stepper.steps[self.step_state]
        self.step_name = name
        func(self)
        self.step_state = (self.step_state+1) % len(aztec_circle_stepper.steps)

from aztec_circle import aztec
from simple_scene_reactor import simple_scene_reactor
from step_scene_reactor import step_scene_reactor
from tile_generator import sequence_tile_generator
from qt_helpers import *

class aztec_scene:
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

    def _step0(self):
        self.az.reactor.start_grow(self.az)
        self.az.increase_size()

    def _step1(self):
        self.az.find_collisions()

    def _step2(self):
        self.az.remove_collisions()

    def _step3(self):
        self.az.move_tiles()

    def _step4(self):
        self.az.fill_holes()
        self.az.reactor.end_grow(self.az)

    steps = {
        0: (_step0, "Grow diamond"),
        1: (_step1, "Find collisions"),
        2: (_step2, "Remove collisions"),
        3: (_step3, "Move tiles"),
        4: (_step4, "Fill holes"),
    }

    def step(self):
        func, name = aztec_scene.steps[self.step_state]
        self.step_name = name
        func(self)
        self.step_state = (self.step_state+1) % len(aztec_scene.steps)
       
app = create_app()

az_scene = aztec_scene()
steps = list(map(lambda i: i[1][1], sorted(aztec_scene.steps.items())))

control_dock, control_layout = create_dock("Controls")

step_name_list = create_list("Current Step", steps, control_layout)
step_button = create_button("Step", control_layout)
play_button = create_button("Play", control_layout)
stop_button = create_button("Stop", control_layout)
reset_button = create_button("Reset", control_layout)
delay_box = create_number_range("Step delay (ms)", 0, 1000, 20, control_layout)
add_stretch(control_layout)

gen_dock, gen_layout = create_dock("Tiles Generation")

gen_sequence = create_text("Tiles sequence (h, v, r)", "hvr vvhrr", az_scene.generator.sequence(), gen_layout)
seed_box = create_number_text("Random seed", 0, 2000000000, az_scene.generator.random_seed, gen_layout)
add_stretch(gen_layout)

window = create_main_window("Aztec Artic Circle", az_scene.scene_react.view)
add_dock(window, control_dock)
add_dock(window, gen_dock)

timer = create_timer(int(delay_box.value()))

def update_step_name():
    select_in_list(az_scene.step_name, step_name_list)

@reset_button.clicked.connect
def on_reset():
    az_scene.reset()

@step_button.clicked.connect
def on_step():
    az_scene.step()
    update_step_name()

@play_button.clicked.connect
def on_play():
    timer.start()

@stop_button.clicked.connect
def on_stop():
    timer.stop()

@delay_box.valueChanged.connect
def on_delay_changed(value):
    timer.setInterval(value)

@seed_box.textChanged.connect
def on_seed(value):
    try:
        new_seed = int(value)
    except:
        return
    az_scene.generator.seed = new_seed

@gen_sequence.textChanged.connect
def on_sequence(value):
    az_scene.generator.set_sequence(value)

@timer.timeout.connect
def on_timer():
    az_scene.step()
    update_step_name()

start_app(app, window)


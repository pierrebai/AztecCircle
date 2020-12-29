from aztec_scene_widget import aztec_scene_widget
from qt_helpers import *

app = create_app()

az_scene = aztec_scene_widget()
steps = list(map(lambda i: i[1][1], sorted(az_scene.steps.items())))

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

stats_dock, stats_layout = create_dock("Statistics")

tiles_count_label = create_text("Tiles count: ", str(0), str(0), stats_layout)
tiles_count_label.setEnabled(False)
add_stretch(stats_layout)

window = create_main_window("Aztec Artic Circle", az_scene.scene_react.view)
add_dock(window, control_dock)
add_dock(window, gen_dock)
add_dock(window, stats_dock)

timer = create_timer(int(delay_box.value()))

def aztec_step():
    az_scene.step()
    select_in_list(az_scene.step_name, step_name_list)
    tiles_count_label.setText(str(az_scene.az.count_tiles()))

@reset_button.clicked.connect
def on_reset():
    az_scene.reset()

@step_button.clicked.connect
def on_step():
    aztec_step()

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
    aztec_step()

start_app(app, window)


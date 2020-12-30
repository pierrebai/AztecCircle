from aztec_circle import aztec_circle_stepper
from reactor import step_scene_reactor
from reactor import simple_scene_reactor
from reactor import canvas_reactor
from qt_helpers import *

app = create_app()

reactor = step_scene_reactor(True)
#reactor = simple_scene_reactor()
#reactor = canvas_reactor()
stepper = aztec_circle_stepper(reactor)
steps = list(map(lambda i: i[1][1], sorted(stepper.steps.items())))

control_dock, control_layout = create_dock("Controls")

step_name_list = create_list("Current Step", steps, control_layout)
step_button = create_button("Step", control_layout)
play_button = create_button("Play", control_layout)
stop_button = create_button("Stop", control_layout)
reset_button = create_button("Reset", control_layout)
delay_box = create_number_range("Step delay (ms)", 0, 1000, 20, control_layout)
add_stretch(control_layout)

gen_dock, gen_layout = create_dock("Tiles Generation")

gen_sequence = create_text("Tiles sequence (h, v, r)", "hvr vvhrr", stepper.generator.sequence(), gen_layout)
seed_box = create_number_text("Random seed", 0, 2000000000, stepper.generator.random_seed, gen_layout)
add_stretch(gen_layout)

stats_dock, stats_layout = create_dock("Statistics")

tiles_count_label = create_text("Tiles count", str(0), str(0), stats_layout)
tiles_count_label.setEnabled(False)
frozen_blue_count_label = create_text("Frozen blue", str(0), str(0), stats_layout)
frozen_blue_count_label.setEnabled(False)
frozen_yellow_count_label = create_text("Frozen yellow", str(0), str(0), stats_layout)
frozen_yellow_count_label.setEnabled(False)
frozen_green_count_label = create_text("Frozen green", str(0), str(0), stats_layout)
frozen_green_count_label.setEnabled(False)
frozen_red_count_label = create_text("Frozen red", str(0), str(0), stats_layout)
frozen_red_count_label.setEnabled(False)
pi_approximation_label = create_text("PI approximation", str(0), str(0), stats_layout)
pi_approximation_label.setEnabled(False)
add_stretch(stats_layout)

window = create_main_window("Aztec Artic Circle", reactor.widget())
add_dock(window, control_dock)
add_dock(window, gen_dock)
add_dock(window, stats_dock)

timer = create_timer(int(delay_box.value()))

def aztec_step():
    stepper.step()
    select_in_list(stepper.step_name, step_name_list)
    tiles_count_label.setText(str(stepper.az.count_tiles()))
   
    yc, rc, bc, gc = stepper.az.count_frozen_tiles_by_type()
    frozen_yellow_count_label.setText(str(yc))
    frozen_red_count_label.setText(str(rc))
    frozen_blue_count_label.setText(str(bc))
    frozen_green_count_label.setText(str(gc))

    if stepper.step_state == 0:
        total_frozen = yc + rc + bc + gc
        pi_approximation = 4. * (1. - (total_frozen / stepper.az.count_tiles()))
        pi_approximation_label.setText(str(pi_approximation))

@reset_button.clicked.connect
def on_reset():
    stepper.reset()

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
    stepper.generator.seed = new_seed

@gen_sequence.textChanged.connect
def on_sequence(value):
    stepper.generator.set_sequence(value)

@timer.timeout.connect
def on_timer():
    aztec_step()

start_app(app, window)


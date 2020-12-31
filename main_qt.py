from aztec_circle import aztec_circle_stepper
from reactor.qt import anim_scene_reactor
from reactor.qt import step_scene_reactor
from reactor.qt import simple_scene_reactor
from reactor.qt import canvas_reactor
from qt_helpers import *

app = create_app()

timer = create_timer(1)
timer.setSingleShot(True)
playing = False

reactor = anim_scene_reactor(lambda: playing and timer.start(), 500, True)
#reactor = step_scene_reactor(True)
#reactor = simple_scene_reactor()
#reactor = canvas_reactor()
stepper = aztec_circle_stepper(reactor)
steps = list(map(lambda i: i[1][1], sorted(stepper.steps.items())))

control_dock, control_layout = create_dock("Play Controls")

step_name_list = create_list("Current Step", steps, control_layout)
step_button = create_button("Step", control_layout)
play_button = create_button("Play", control_layout)
stop_button = create_button("Stop", control_layout)
reset_button = create_button("Reset", control_layout)
delay_box = create_number_range("Step delay (ms)", 0, 10000, 500, control_layout)
add_stretch(control_layout)

anim_dock, anim_layout = create_dock("Animation Controls")

animate_option = create_option("Animate", anim_layout)
animate_limit_box = create_number_range("Stop Animating After Generation #", 0, 10000, reactor.animate_limit, anim_layout)
show_arrow_option = create_option("Show movement arrow", anim_layout)
show_cross_option = create_option("Show collision cross", anim_layout)
add_stretch(anim_layout)

gen_dock, gen_layout = create_dock("Tiles Generation")

gen_sequence = create_text("Tiles sequence (h, v, r)", "hvr vvhrr", stepper.generator.sequence(), gen_layout)
seed_box = create_number_text("Random seed", 0, 2000000000, stepper.generator.random_seed, gen_layout)
add_stretch(gen_layout)

stats_dock, stats_layout = create_dock("Statistics")

generation_label = create_read_only_text("Generation", str(0), str(0), stats_layout)
tiles_count_label = create_read_only_text("Tiles count", str(0), str(0), stats_layout)
frozen_blue_count_label = create_read_only_text("Frozen blue", str(0), str(0), stats_layout)
frozen_yellow_count_label = create_read_only_text("Frozen yellow", str(0), str(0), stats_layout)
frozen_green_count_label = create_read_only_text("Frozen green", str(0), str(0), stats_layout)
frozen_red_count_label = create_read_only_text("Frozen red", str(0), str(0), stats_layout)
pi_approximation_label = create_read_only_text("PI approximation", str(0), str(0), stats_layout)
add_stretch(stats_layout)

window = create_main_window("Aztec Artic Circle", reactor.widget())
add_dock(window, control_dock)
add_dock(window, anim_dock)
add_dock(window, gen_dock)
add_dock(window, stats_dock)


def aztec_step():
    stepper.step()
    select_in_list(stepper.step_name, step_name_list)

    generation_label.setText(str(stepper.az.size()))
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
    global playing
    playing = True
    timer.start()

@stop_button.clicked.connect
def on_stop():
    global playing
    playing = False
    timer.stop()

@delay_box.valueChanged.connect
def on_delay_changed(value):
    reactor.anim_duration = int(value)

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

@animate_option.stateChanged.connect
def on_animate(state):
    reactor.animate = bool(state)

@animate_limit_box.valueChanged.connect
def on_animate_limit_changed(value):
    reactor.animate_limit = int(value)

@show_arrow_option.stateChanged.connect
def on_show_arrow(state):
    reactor.show_movement_arrow = bool(state)

@show_cross_option.stateChanged.connect
def on_animate(state):
    reactor.show_collision_cross = bool(state)

@timer.timeout.connect
def on_timer():
    aztec_step()

start_app(app, window)


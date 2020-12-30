from reactor import recording_player
from reactor import anim_scene_reactor
from reactor import step_scene_reactor
from qt_helpers import *

import sys

anim_duration  = int(sys.argv[1]) if len(sys.argv) > 1 else 1000

app = create_app()
timer = create_timer(1)
reactor = anim_scene_reactor(timer, anim_duration, True) if anim_duration else step_scene_reactor(True)
window = create_main_window("Aztec Artic Circle", reactor.widget())

player = recording_player(reactor)

if anim_duration:
    timer.setSingleShot(True)

@timer.timeout.connect
def on_timer():
    player.step()
    if anim_duration:
        if not reactor.anim_done:
            timer.start()

timer.start()

start_app(app, window)

from reactor import recording_player
from reactor import step_scene_reactor
from qt_helpers import *

app = create_app()
reactor = step_scene_reactor(True)
window = create_main_window("Aztec Artic Circle", reactor.widget())
timer = create_timer(1)

player = recording_player(reactor)

@timer.timeout.connect
def on_timer():
    player.step()

timer.start()

start_app(app, window)

from aztec_circle import aztec
from simple_scene_reactor import simple_scene_reactor
from step_scene_reactor import step_scene_reactor
from repeatable_random import repeatable_random

from PyQt5.QtCore import QTimer, Qt, QRectF
from PyQt5.QtWidgets import *

import sys

app = QApplication(sys.argv)

scene = QGraphicsScene()

scene_view = QGraphicsView(scene)
scene_view.setInteractive(False)
scene_view.setResizeAnchor(QGraphicsView.AnchorViewCenter)
scene_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
scene_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

scene_react = step_scene_reactor(scene, scene_view)
#scene_react = simple_scene_reactor(scene, scene_view)

window = QMainWindow()
window.setWindowTitle("Aztec Artic Circle")
window.resize(800, 600)
window.setCentralWidget(scene_view)
window.show()

seed = 7
az = aztec(0, repeatable_random(seed), scene_react)

timer = QTimer()
timer.setInterval(20)
timer.start()
timer_state = 0

@timer.timeout.connect
def on_timer():
    action = {
        0: lambda: az.reactor.start_grow(az),
        1: lambda: az._increase_size(),
        2: lambda: az._remove_collisions(),
        3: lambda: az._move_tiles(),
        4: lambda: az._fill_holes(),
        5: lambda: az.reactor.end_grow(az),
    }
    global timer_state
    func = action[timer_state]
    func()
    timer_state = (timer_state+1) % 6

app.exec_()


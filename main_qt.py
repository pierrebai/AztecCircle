from aztec_circle import aztec
from simple_scene_reactor import simple_scene_reactor
from step_scene_reactor import step_scene_reactor
from repeatable_random import repeatable_random

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import *

import sys

class aztec_scene:
    def __init__(self, scene, scene_view):
        self.scene_react = step_scene_reactor(scene, scene_view)
        #scene_react = simple_scene_reactor(scene, scene_view)
        self.seed = 7
        self.reset()
        self.timer = QTimer()
        self.timer.setInterval(20)
        self.timer.timeout.connect(lambda: self.step())

    def reset(self):
        self.step_state = 0
        self.scene_react.reset()
        self.az = aztec(1, repeatable_random(self.seed), self.scene_react)

    def _step0(self):
        self.az.reactor.start_grow(self.az)
        self.az.increase_size()

    def _step1(self):
        self.az._remove_collisions()

    def _step2(self):
        self.az.move_tiles()

    def _step3(self):
        self.az.fill_holes()
        self.az.reactor.end_grow(self.az)

    def step(self):
        actions = {
            0: self._step0,
            1: self._step1,
            2: self._step2,
            3: self._step3,
        }
        func = actions[self.step_state]
        func()
        self.step_state = (self.step_state+1) % len(actions)

    def play(self):
        self.timer.start()

    def stop(self):
        self.timer.stop()
        

app = QApplication(sys.argv)

scene = QGraphicsScene()

scene_view = QGraphicsView(scene)
scene_view.setInteractive(False)
scene_view.setResizeAnchor(QGraphicsView.AnchorViewCenter)
scene_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
scene_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

control_dock = QDockWidget("Controls")
control_dock.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
control_container = QWidget()
control_layout = QVBoxLayout(control_container)
control_dock.setWidget(control_container)

reset_button = QPushButton("Reset")
control_layout.addWidget(reset_button)

step_button = QPushButton("Step")
control_layout.addWidget(step_button)

play_button = QPushButton("Play")
control_layout.addWidget(play_button)

stop_button = QPushButton("Stop")
control_layout.addWidget(stop_button)

control_layout.addStretch()

window = QMainWindow()
window.setWindowTitle("Aztec Artic Circle")
window.resize(800, 600)
window.setCentralWidget(scene_view)
window.addDockWidget(Qt.LeftDockWidgetArea, control_dock)
window.show()

az_scene = aztec_scene(scene, scene_view)

@reset_button.clicked.connect
def on_reset():
    az_scene.reset()

@step_button.clicked.connect
def on_step():
    az_scene.step()

@play_button.clicked.connect
def on_play():
    az_scene.play()

@stop_button.clicked.connect
def on_stop():
    az_scene.stop()
    
app.exec_()


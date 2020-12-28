from aztec_circle import aztec
from simple_scene_reactor import simple_scene_reactor
from step_scene_reactor import step_scene_reactor
from repeatable_random import repeatable_random

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator

import sys

class aztec_scene:
    def __init__(self):
        self.scene_react = step_scene_reactor()
        #scene_react = simple_scene_reactor()
        self.seed = 7
        self.step_name = ""
        self.reset()

    def reset(self):
        self.step_state = 0
        self.scene_react.reset()
        self.az = aztec(1, repeatable_random(self.seed), self.scene_react)

    def _step0(self):
        self.step_name = "Grow diamond"
        self.az.reactor.start_grow(self.az)
        self.az.increase_size()

    def _step1(self):
        self.step_name = "Find collisions"
        self.az.find_collisions()

    def _step2(self):
        self.step_name = "Remove collisions"
        self.az.remove_collisions()

    def _step3(self):
        self.step_name = "Move tiles"
        self.az.move_tiles()

    def _step4(self):
        self.step_name = "Fill holes"
        self.az.fill_holes()
        self.az.reactor.end_grow(self.az)

    def step(self):
        actions = {
            0: self._step0,
            1: self._step1,
            2: self._step2,
            3: self._step3,
            4: self._step4,
        }
        func = actions[self.step_state]
        func()
        self.step_state = (self.step_state+1) % len(actions)
       
app = QApplication(sys.argv)

az_scene = aztec_scene()

control_dock = QDockWidget("Controls")
control_dock.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
control_container = QWidget()
control_container.setMinimumWidth(150)
control_layout = QVBoxLayout(control_container)
control_dock.setWidget(control_container)

step_name_label = QLabel("Step:")
control_layout.addWidget(step_name_label)

reset_button = QPushButton("Reset")
control_layout.addWidget(reset_button)

step_button = QPushButton("Step")
control_layout.addWidget(step_button)

play_button = QPushButton("Play")
control_layout.addWidget(play_button)

stop_button = QPushButton("Stop")
control_layout.addWidget(stop_button)

delay_label = QLabel()
delay_label.setText("Step delay")
control_layout.addWidget(delay_label)

delay_box = QSpinBox()
delay_box.setRange(0, 1000)
delay_box.setValue(20)
control_layout.addWidget(delay_box)

seed_label = QLabel()
seed_label.setText("Random seed")
control_layout.addWidget(seed_label)

seed_box = QLineEdit()
seed_box.setValidator(QIntValidator(0, 2000000000))
seed_box.setText(str(az_scene.seed))
control_layout.addWidget(seed_box)

control_layout.addStretch()

window = QMainWindow()
window.setWindowTitle("Aztec Artic Circle")
window.resize(800, 600)
window.setCentralWidget(az_scene.scene_react.view)
window.addDockWidget(Qt.LeftDockWidgetArea, control_dock)
window.show()

timer = QTimer()
timer.setInterval(delay_box.value())


def update_step_name():
    step_name_label.setText("Step: " + az_scene.step_name)

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
    az_scene.seed = new_seed
    az_scene.reset()

@timer.timeout.connect
def on_timer():
    az_scene.step()
    update_step_name()

az_scene.reset()
app.exec_()


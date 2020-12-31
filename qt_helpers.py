from PyQt5.QtCore import QTimer, Qt, QMargins
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator

import sys

def create_app():       
    return QApplication(sys.argv)

def start_app(app: QApplication, window: QMainWindow):
    window.show()
    app.exec_()

def create_dock(title: str) -> (QDockWidget, QVBoxLayout):
    dock = QDockWidget(title)
    dock.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
    container = QWidget()
    container.setMinimumWidth(150)
    layout = QVBoxLayout(container)
    dock.setWidget(container)
    return dock, layout

def create_label(title: str, layout: QLayout) -> QLabel:
    widget = QLabel(title)
    layout.addWidget(widget)
    return widget

def create_list(title: str, contents: list, layout: QLayout, enabled = False) -> QListWidget:
    create_label(title, layout)
    widget = QListWidget()
    widget.setEnabled(enabled)
    for name in contents:
        widget.addItem(name)
    layout.addWidget(widget)
    return widget

def select_in_list(name: str, widget: QListWidget):
    items = widget.findItems(name, Qt.MatchExactly)
    if len(items) > 0:
        widget.setCurrentItem(items[0])

def create_button(title: str, layout: QLayout) -> QPushButton:
    widget = QPushButton(title)
    layout.addWidget(widget)
    return widget

def create_number_range(title: str, low: int, high: int, value: int, layout: QLayout) -> QSpinBox:
    create_label(title, layout)
    widget = QSpinBox()
    widget.setRange(low, high)
    widget.setValue(value)
    layout.addWidget(widget)
    return widget

def create_text(title: str, example: str, value: str, layout: QLayout) -> QLineEdit:
    container = QWidget()
    container_layout = QHBoxLayout(container)
    container_layout.setContentsMargins(0, 0, 0, 0)
    create_label(title, container_layout)
    widget = QLineEdit()
    widget.setText(value)
    widget.setPlaceholderText(example)
    container_layout.addWidget(widget)
    layout.addWidget(container)
    return widget

def create_read_only_text(title: str, example: str, value: str, layout: QLayout) -> QLineEdit:
    widget = create_text(title, example, value, layout)
    widget.setEnabled(False)
    return widget

def create_number_text(title: str, low: int, high: int, value: int, layout: QLayout) -> QLineEdit:
    widget = create_text(title, str((low + high)/2), str(value), layout)
    widget.setValidator(QIntValidator(low, high))
    return widget

def add_stretch(layout: QLayout):
    layout.addStretch()

def create_main_window(title: str, central_widget) -> QMainWindow:
    window = QMainWindow()
    window.setWindowTitle(title)
    window.resize(800, 600)
    window.setCentralWidget(central_widget)
    return window

def add_dock(window: QMainWindow, dock: QDockWidget):
    window.addDockWidget(Qt.LeftDockWidgetArea, dock)

def create_timer(interval: int) -> QTimer:
    timer = QTimer()
    timer.setInterval(interval)
    return timer

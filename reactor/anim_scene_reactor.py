from .step_scene_reactor import step_scene_reactor
from .qt_drawings import qt_drawings

from PyQt5.QtCore import QVariant, QVariantAnimation, QPointF

import math


class anim_scene_reactor(step_scene_reactor):
    """
    Reactor using a Qt graphics scene to show animated step-by-step changes.
    """

    def __init__(self, timer, anim_duration, *args, **kwargs):
        super(anim_scene_reactor, self).__init__(*args, **kwargs)
        self.timer = timer
        self.anim_duration = anim_duration
        self.anim_duration_speedup = 1.
        self.anim_done = None
        self.anim_value_changed = None
        self.anim = None
        self.cross = anim_scene_reactor.create_cross()

    #################################################################
    #
    # Animations

    def _prepare_anim(self, x, y, duration_fraction = 1):
        item = self.items[x][y] or self.new_items[x][y]
        anim = QVariantAnimation()
        anim.setDuration(self.anim_duration * duration_fraction * self.anim_duration_speedup)
        anim.finished.connect(self._on_anim_finished)
        anim.valueChanged.connect(self._on_anim_value_changed)
        self.anim = anim
        return item, anim

    def _on_anim_finished(self):
        #print('anim finished')
        if self.anim_done:
            self.anim_done()
        self.timer.start()

    def _on_anim_value_changed(self, value):
        #print(f'anim value changed {value}')
        if self.anim_value_changed:
            self.anim_value_changed(value)

    #################################################################
    #
    # Reactor

    def increase_size(self, az, origin, size):
        super(anim_scene_reactor, self).increase_size(az, origin, size)
        self.anim_duration_speedup = 1. / size

    def collision(self, az, x, y):
        center = self.center
        self.cross.setPos(*self.pos_to_scene(x - center, y - center))
        self.scene.addItem(self.cross)

        item, anim = self._prepare_anim(x, y, 0.5)
        anim.setStartValue(QVariant(1.))
        anim.setEndValue(QVariant(0.))
        self.anim_value_changed = lambda value: item.setOpacity(value)
        self.anim_done = lambda: self.collision_anim_done(az, x, y)
        anim.start(QVariantAnimation.DeleteWhenStopped)
        #print('collision anim started')

    def collision_anim_done(self, az, x, y):
        #print('collision anim finished')
        super(anim_scene_reactor, self).collision(az, x, y)
        self.scene.removeItem(self.cross)
        self.anim_done = None
        self.anim_value_changed = None

    def move(self, az, x1, y1, x2, y2):
        item, anim = self._prepare_anim(x1, y1)
        center = self.center
        anim.setStartValue(QVariant(QPointF(*self.pos_to_scene(x1 - center, y1 - center))))
        anim.setEndValue(QVariant(QPointF(*self.pos_to_scene(x2 - center, y2 - center))))
        self.anim_value_changed = lambda value: item.setPos(value)
        self.anim_done = lambda: self.move_anim_done(az, x1, y1, x2, y2)
        anim.start(QVariantAnimation.DeleteWhenStopped)
        #print('move anim started')

    def move_anim_done(self, az, x1, y1, x2, y2):
        #print('move anim finished')
        super(anim_scene_reactor, self).move(az, x1, y1, x2, y2)
        self.anim_done = None
        self.anim_value_changed = None

    def fill(self, az, x, y, tile):
        super(anim_scene_reactor, self).fill(az, x, y, tile)

        item, anim = self._prepare_anim(x, y, 0.5)
        item.setOpacity(0.)
        anim.setStartValue(QVariant(0.))
        anim.setEndValue(QVariant(1.))
        self.anim_value_changed = lambda value: item.setOpacity(value)
        self.anim_done = lambda: self.fill_anim_done(az, x, y, tile)
        anim.start(QVariantAnimation.DeleteWhenStopped)
        #print('fill anim started')
        
    def fill_anim_done(self, az, x, y, tile):
        #print('fill anim finished')
        self.anim_done = None
        self.anim_value_changed = None

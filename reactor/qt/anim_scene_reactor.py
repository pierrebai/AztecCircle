from .step_scene_reactor import step_scene_reactor
from .qt_drawings import qt_drawings

from PyQt5.QtCore import QVariant, QVariantAnimation, QPointF

import math


class anim_scene_reactor(step_scene_reactor):
    """
    Reactor using a Qt graphics scene to show animated step-by-step changes.
    """

    def __init__(self, anim_done_callback, anim_duration, *args, **kwargs):
        super(anim_scene_reactor, self).__init__(*args, **kwargs)
        self.anim_done_callback = anim_done_callback
        self.anim_duration = anim_duration
        self.anim_duration_speedup = 1.
        self.anims = set()


    #################################################################
    #
    # Animations

    def _prepare_anim(self, item, start_value, end_value, on_changed, on_finished, duration_fraction = 1.):
        anim = QVariantAnimation()
        self.anims.add(anim)
        anim.setDuration(self.anim_duration * duration_fraction * self.anim_duration_speedup)
        anim.setStartValue(QVariant(start_value))
        anim.setEndValue(QVariant(end_value))
        if on_changed:
            anim.valueChanged.connect(on_changed)
        if on_finished:
            anim.finished.connect(on_finished)
        anim.finished.connect(lambda: self._remove_anim(anim))
        anim.start()
        return anim

    def _remove_anim(self, anim):
        self.anims.remove(anim)
        self._check_all_anims_done()

    def _check_all_anims_done(self):
        if self.anim_done_callback and not self.anims:
            self.anim_done_callback()

    #################################################################
    #
    # Reactor

    def reallocate(self, az, old_amount: int, new_amount: int):
        super(anim_scene_reactor, self).reallocate(az, old_amount, new_amount)
        self._check_all_anims_done()

    def increase_size(self, az, origin, size):
        super(anim_scene_reactor, self).increase_size(az, origin, size)
        self.anim_duration_speedup = 1. / math.sqrt(size / 4)
        self._check_all_anims_done()

    def collision(self, az, x, y):
        center = self.center
        tile = az.tiles()[x][y] if az else None
        cross = anim_scene_reactor.create_cross()
        cross.setPos(*self.middle_pos_to_scene(x - center, y - center, tile))
        self.scene.addItem(cross)

        item = self.items[x][y]
        if not item:
            raise Exception()
        anim = self._prepare_anim(item, 1., 0.,
            lambda value: item.setOpacity(value),
            lambda: self._collision_anim_done(item, cross)
        )

    def _collision_anim_done(self, item, cross):
        self.scene.removeItem(item)
        self.scene.removeItem(cross)

    def collisions_done(self, az):
        super(anim_scene_reactor, self).collisions_done(az)
        self._check_all_anims_done()

    def move(self, az, x1, y1, x2, y2):
        center = self.center
        tile = az.tiles()[x1][y1] if az else None
        arrow = anim_scene_reactor.create_arrow(tile)
        arrow.setPos(*self.middle_pos_to_scene(x1 - center, y1 - center, tile))
        self.scene.addItem(arrow)
        anim = self._prepare_anim(arrow,
            QPointF(*self.middle_pos_to_scene(x1 - center, y1 - center, tile)),
            QPointF(*self.middle_pos_to_scene(x2 - center, y2 - center, tile)),
            lambda value: arrow.setPos(value),
            lambda: self.scene.removeItem(arrow)
        )

        item = self.items[x1][y1]
        if not item:
            raise Exception()
        self.new_items[x2][y2] = item
        anim = self._prepare_anim(item,
            QPointF(*self.pos_to_scene(x1 - center, y1 - center)),
            QPointF(*self.pos_to_scene(x2 - center, y2 - center)),
            lambda value: item.setPos(value),
            None
        )

    def moves_done(self, az):
        super(anim_scene_reactor, self).moves_done(az)
        self._check_all_anims_done()

    def fill(self, az, x, y, tile):
        super(anim_scene_reactor, self).fill(az, x, y, tile)

        item = self.new_items[x][y]
        if not item:
            raise Exception()
        item.setOpacity(0.)

        anim = self._prepare_anim(item, 0., 1.,
            lambda value: item.setOpacity(value),
            None
        )
        
    def fills_done(self, az):
        super(anim_scene_reactor, self).fills_done(az)
        self._check_all_anims_done()

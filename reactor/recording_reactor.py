from .reactor import reactor
from .recorder import file_recorder, file_player
from aztec_circle import half_tile

class recording_reactor(reactor):
    """
    Write all changes to a file in a short format
    with the same line length for all actions.
    """
    def __init__(self, recorder = None):
        self.recorder = recorder if recorder else file_recorder()
        self.center = 0

    def reset(self):
        self.recorder.reset()

    def output(self, text):
        self.recorder.output(text)

    def reallocate(self, az, old_amount, new_amount):
        self.output(f"R {old_amount} {new_amount}")
        self.center = new_amount // 2

    def increase_size(self, az, origin, size):
        origin = -size
        self.output(f"I {origin:>8} {size:>8}")

    def collision(self, az, x, y):
        org = self.center
        x -= org
        y -= org
        self.output(f"C {x:>8} {y:>8}")

    def collisions_done(self, az):
        self.output(f"E collisions")

    def move(self, az, x1, y1, x2, y2):
        org = self.center
        x1 -= org
        y1 -= org
        x2 -= org
        y2 -= org
        self.output(f"M {x1:>8} {y1:>8} {x2:>8} {y2:>8}")

    def moves_done(self, az):
        self.output("E moves")

    def fill(self, az, x, y, tile):
        org = self.center
        x -= org
        y -= org
        text = recording_reactor._tile_to_text(tile)
        self.output(f"F {x:>8} {y:>8} {text}")

    @staticmethod
    def _tile_to_text(tile):
        return ' '.join([
            'vh'[tile.is_horizontal],
            'lh'[tile.is_first_part],
            'mf'[tile.is_frozen],
            'du'[tile.is_positive],
        ])

    def fills_done(self, az):
        self.output("E fills")

class recording_player:
    def __init__(self, reactor, player = None):
        self.reactor = reactor
        self.player = player if player else file_player()

    def _replay_reallocate(self, parts):
        az = None
        old_amount, new_amount = tuple(map(int, parts))
        self.reactor.reallocate(az, old_amount, new_amount)

    def _replay_increase_size(self, parts):
        az = None
        origin, size = tuple(map(int, parts))
        self.reactor.increase_size(az, origin, size)

    def _replay_collision(self, parts):
        az = None
        x, y = tuple(map(int, parts))
        self.reactor.collision(az, x, y)

    def _replay_collisions_done(self):
        az = None
        self.reactor.collisions_done(az)

    def _replay_move(self, parts):
        az = None
        x1, y1, x2, y2 = tuple(map(int, parts))
        self.reactor.move(az, x1, y1, x2, y2)

    def _replay_moves_done(self):
        az = None
        self.reactor.moves_done(az)

    def _replay_fill(self, parts):
        az = None
        x, y = tuple(map(int, parts[0:2]))
        tile = recording_player._text_to_tile(parts[2:])
        self.reactor.fill(az, x, y, tile)

    @staticmethod
    def _text_to_tile(parts):
        horiz  = (parts[0] == 'h')
        high   = (parts[1] == 'h')
        frozen = (parts[2] == 'f')
        pos    = (parts[3] == 'u')
        tile = half_tile(horiz, pos, high)
        tile.is_frozen = frozen
        return tile

    def _replay_fills_done(self):
        az = None
        self.reactor.fills_done(az)

    done_funcs = {
        'c': _replay_collisions_done,
        'm': _replay_moves_done,
        'f': _replay_fills_done,
    }

    def _replay_end(self, parts):
        func = recording_player.done_funcs[parts[0][0]]
        func(self)

    replay_funcs = {
        'R': _replay_reallocate,
        'I': _replay_increase_size,
        'C': _replay_collision,
        'M': _replay_move,
        'F': _replay_fill,
        'E': _replay_end,
    }
    
    def step(self):
        line = self.player.input()
        if line:
            parts = line.split()
            func = recording_player.replay_funcs[parts[0]]
            func(self, parts[1:])
        

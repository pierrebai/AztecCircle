import sys

class reactor:
    """
    React to changes in an aztec circle diamond.
    """

    def reallocate(self, az, old_amount, new_amount):
        """
        Called when the axtec diamond reallocates its tiles.
        The aztec.reallocate_data() function can be used to similarly reallocate your lists.
        """
        pass

    def increase_size(self, az, size):
        """
        Called after the aztec diamond size has been increased and its tiles recentered.
        """
        pass

    def collision(self, az, x, y):
        """
        Called when the tiles at the given position are about to collide.
        (Called before the tiles are removed.)
        """
        pass

    def collisions_done(self, az):
        """
        Called when the all collisions are done.
        """
        pass

    def move(self, az, x1, y1, x2, y2):
        """
        Called when a tile is about to move from one position to another.
        """
        pass

    def moves_done(self, az):
        """
        Called when the all movements are done.
        """
        pass

    def fill(self, az, x, y, tile):
        """
        Called when a new tile has been added to fill a hole.
        """
        pass

    def fills_done(self, az):
        """
        Called when the all hole fillings are done.
        """
        pass


class recording_reactor(reactor):
    """
    Write all changes to a file in a short format
    with the same line length for all actions.
    """
    def __init__(self, file = sys.stdout):
        self.file = file
        self.center = 0

    def reset(self):
        self.file.seek(0)

    def output(self, text):
        print(f"{text:40}", file=self.file)

    def reallocate(self, az, old_amount, new_amount):
        self.output(f"R {old_amount} {new_amount}")
        self.center = new_amount // 2

    def increase_size(self, az, size):
        self.output(f"I {size:>8}")

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
            'lh'[tile.is_high_part],
            'mf'[tile.is_frozen],
            'du'[tile.is_positive],
        ])

    def fills_done(self, az):
        self.output("E fills")


class debug_reactor(reactor):
    """
    Write all changes to a file.
    """
    def __init__(self, file = sys.stdout):
        self.file = file
        self.center = 0

    def reset(self):
        self.file.seek(0)

    def output(self, text):
        print(text, file=self.file)

    def reallocate(self, az, old_amount, new_amount):
        self.output(f"Reallocate from {old_amount} to {new_amount}")
        self.center = new_amount // 2

    def increase_size(self, az, size):
        self.output(f"Increase size to {size}")

    def collision(self, az, x, y):
        org = self.center
        x -= org
        y -= org
        self.output(f"Collision at {x}/{y}")

    def collisions_done(self, az):
        self.output(f"End collisions")

    def move(self, az, x1, y1, x2, y2):
        org = self.center
        x1 -= org
        y1 -= org
        x2 -= org
        y2 -= org
        self.output(f"Move from {x1}/{y1} to {x2}/{y2}")

    def moves_done(self, az):
        self.output("End moves")

    def fill(self, az, x, y, tile):
        org = self.center
        x -= org
        y -= org
        text = recording_reactor._tile_to_text(tile)
        self.output(f"Fill at {x}/{y} {text}")

    @staticmethod
    def _tile_to_text(tile):
        return ' '.join([
            ['verti',  'horiz' ][tile.is_horizontal],
            ['low ',   'high'  ][tile.is_high_part],
            ['moving', 'frozen'][tile.is_frozen],
            ['down',   'up  '  ][tile.is_positive],
        ])

    def fills_done(self, az):
        self.output("End fills")

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
        text = debug_reactor._tile_to_text(tile)
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

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

    def start_grow(self, az):
        """
        Called before the aztec diamond grows.
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

    def move(self, az, x1, y1, x2, y2):
        """
        Called when a tile is about to move from one position to another.
        """
        pass

    def fill(self, az, x, y, tile):
        """
        Called when a new tile has been added.
        """
        pass

    def end_grow(self, az):
        """
        Called after the aztec diamond has grown.
        """
        pass


class debug_reactor(reactor):
    def reallocate(self, az, old_amount, new_amount):
        print(f"Reallocate from {old_amount} to {new_amount}")

    def start_grow(self, az):
        print("Start grow")

    def increase_size(self, az, size):
        print(f"Increase size to {size}")

    def collision(self, az, x, y):
        print(f"Remove collision at {x}/{y}")

    def move(self, az, x1, y1, x2, y2):
        print(f"Move from {x1}/{y1} to {x2}/{y2}")

    def fill(self, az, x, y, tile):
        print(f"Fill at {x}/{y}")

    def end_grow(self, az):
        print("End grow")

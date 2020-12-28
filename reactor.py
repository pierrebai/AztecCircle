class reactor:
    """
    React to changes in an aztec circle diamond.
    """

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

    def collision_found(self, az, pos):
        """
        Called when the tiles at the given position are about to collide.
        (Called before the tiles are removed.)
        """
        pass

    def collision_removed(self, az, pos):
        """
        Called when the tile at the given position is about to collide with another.
        (Called after the tile is removed.)
        """
        pass

    def move(self, az, pos1, pos2):
        """
        Called when a tile is about to move from one position to another.
        """
        pass

    def fill(self, az, pos, tile):
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
    def start_grow(self, az):
        print("Start grow")

    def increase_size(self, az, size):
        print(f"Increase size to {size}")

    def collision_found(self, az, pos):
        print(f"Collision at {pos}")

    def collision_removed(self, az, pos):
        print(f"Remove collision at {pos}")

    def move(self, az, pos1, pos2):
        print(f"Move from {pos1} to {pos2}")

    def fill(self, az, pos, tile):
        print(f"Fill at {pos}")

    def end_grow(self, az):
        print("End grow")

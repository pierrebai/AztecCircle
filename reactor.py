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

    def collision(self, az, pos1, pos2):
        """
        Called when the tiles at the given position are about to collide.
        (Called before the tiles are removed.)
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

from random import Random

class tile_generator:
    """
    A generator of tile orientation.
    """

    def is_next_horizontal(self) -> bool:
        """
        Generates the next tile orientation.
        """
        return True

    def reset(self):
        """
        Reset the generator to its initial state.
        """
        pass

class random_tile_generator(tile_generator):
    """
    A random tile generator that can be reset to replay the same random sequence.
    """

    def __init__(self, random_seed: int):
        """
        Create a random tile generator with the given seed.
        """
        self.random_seed = random_seed
        self._rnd = Random(random_seed)

    def is_next_horizontal(self) -> bool:
        """
        Generates the next random tile orientation.
        """
        return self._rnd.randrange(2) == 1

    def reset(self):
        """
        Rewind the random generator to the start.
        """
        self._rnd = Random(self.random_seed)


class sequence_tile_generator(random_tile_generator):
    """
    A tile generator that follow a sequence of tiles, some of which may be random.
    """

    def __init__(self, random_seed: int, sequence: str):
        """
        Create a tile generator that will create the given sequence of tiles
        repeatedly. The sequence is described textually with any number
        letters in h, v, r, which can repeat as desired. The letter means:

           h: horizontal
           v: vertical
           r: random
        """
        super(sequence_tile_generator, self).__init__(random_seed)
        
        self._next_in_sequence = 0
        self.set_sequence(sequence)

    def sequence(self):
        return self._sequence

    def set_sequence(self, sequence: str):
        sequence = sequence if sequence else 'r'
        clean_sequence = list(filter(lambda c: c in 'hvr', sequence.lower()))
        clean_sequence = clean_sequence if clean_sequence else 'r'

        self._sequence = sequence
        self._clean_sequence = clean_sequence
        self._next_in_sequence = 0

    def is_next_horizontal(self) -> bool:
        """
        Generates the next tile orientation.
        """
        letter = self._clean_sequence[self._next_in_sequence]
        self._next_in_sequence = (self._next_in_sequence+1) % len(self._clean_sequence)

        if letter == 'r':
            return super(sequence_tile_generator, self).is_next_horizontal()
        else:
            return letter == 'h'

    def reset(self):
        """
        Rewind the sequence generator to the start of the sequence.
        """
        super(sequence_tile_generator, self).reset()
        self._next_in_sequence = 0

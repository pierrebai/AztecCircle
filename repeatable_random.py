from random import Random

class repeatable_random:
    """
    A random number generator that can be rewind to replay the same random sequence.
    """

    _save_period = 1000

    def __init__(self, seed_value: int):
        """
        Create a repeatable random generator with the given seed.
        """
        self._rnd = Random(seed_value)
        self._count = 0
        self._states = []
        self._save_regularly()

    def next(self) -> bool:
        """
        Save or restore the random state then generates the next random boolean.
        """
        self._save_regularly()
        self._count += 1
        return self._rnd.randrange(2) == 1

    def rewind(self, amount: int = 1):
        """
        Rewind the random generator the given number of values.
        Default to rewinding a single value.
        Rewinding a negative amount goes forward instead.
        """
        target_count = max(0, self._count - amount)
        state_index = min(target_count // repeatable_random._save_period, len(self._states) - 1)
        self._rnd.setstate(self._states[state_index])
        self._count = state_index * repeatable_random._save_period
        while self._count != target_count:
            self.next()

    def _save_regularly(self):
        """
        Regularly save the state of the random number generator
        so that we can go back in time.
        Restore the state if we went back to a previous already-genarated
        value.
        """
        if self._count % repeatable_random._save_period == 0:
            state_index = self._count // repeatable_random._save_period
            while state_index < len(self._states):
                self._states.append(self._rnd.getstate())


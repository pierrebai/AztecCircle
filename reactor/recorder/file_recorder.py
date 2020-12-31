import sys

class file_recorder:
    """
    Record into a file.
    """
    def __init__(self, file = None):
        self.file = file if file else sys.stdout

    def reset(self):
        pass

    def output(self, text):
        print(f"{text:40}", file=self.file)


class file_player:
    """
    Replay from a file.
    """
    def __init__(self, file = None):
        self.file = file if file else sys.stdin

    def input(self):
        return self.file.readline()



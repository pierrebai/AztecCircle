from queue import Queue

class queue_recorder:
    """
    Record into a queue.
    """
    def __init__(self, queue = None):
        self.queue = queue if queue else Queue(1000)

    def reset(self):
        pass

    def output(self, text):
        self.queue.put(text)


class queue_player:
    """
    Replay from a queue.
    """
    def __init__(self, queue):
        if type(queue) is queue_recorder:
            queue = queue.queue
        self.queue = queue

    def input(self):
        return self.queue.get()



from queue import Queue


class QueueHandler:
    def __init__(self, log_queue: Queue):
        self.log_gueue = log_queue

    def add(self, log: str):
        self.log_gueue.put(log)

    def get(self) -> str:
        return self.log_gueue.get(block=False)

class SendUpdateHandler:
    def __init__(self):
        self._queue = None

    @property
    def queue(self):
        return self._queue

    @queue.setter
    def queue(self, log_queue:object):
        self._queue = log_queue

    def send(self, send_list):
        self.queue.put(send_list)

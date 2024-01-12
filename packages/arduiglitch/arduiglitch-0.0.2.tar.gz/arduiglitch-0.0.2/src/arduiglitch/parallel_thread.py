import time
from threading import Thread as Process
from queue import Queue
from typing import Callable, Any
from logger import Log


class ParallelThread:
    def __init__(
        self,
        log: Log,
        function: Callable[[Log, Queue, Any], None],
        *args
    ):
        self.function = function # needs to look like `function(log, control_queue, *args) -> None`
        self.args = args
        self.log = log

        self.process = None
        self.queue = Queue()

    def start(self):
        if (self.process is None) or (not self.process.is_alive()):
            self.process = Process(target=self._thread_fn, name="process", args=(self.log, self.queue, self.args))
            self.process.start()
            self.log.debug(f"Started thread `{self.process.name}`")
        else:
            self.log.critical("Tried to start running thread. Ignoring.")

    def stop(self):
        if (self.process is not None) and (self.process.is_alive()):
            self.queue.put("stop")
            self.process.join()
            self.log.debug("Thread stopped")
        else:
            self.log.critical("Tried to stop unstarted thread. Ignoring.")

    def _thread_fn(self, log, control_queue: Queue, args):
        # Start of thread
        self.log.debug(f"Start of thread; {time.time()}")

        self.function(log, control_queue, *args)

        self.log.debug(f"End of thread; {time.time()}")

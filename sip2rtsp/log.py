import logging
import threading
import queue
from multiprocessing.queues import Queue
from logging import handlers
from setproctitle import setproctitle

def listener_configurer() -> None:
    root = logging.getLogger()
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] %(name)-30s %(levelname)-8s: %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)
    root.setLevel(logging.INFO)

def root_configurer(queue: Queue) -> None:
    h = handlers.QueueHandler(queue)
    root = logging.getLogger()
    root.addHandler(h)
    root.setLevel(logging.INFO)

def log_process(log_queue: Queue) -> None:
    threading.current_thread().name = f"logger"
    setproctitle("sip2rtsp.logger")
    listener_configurer()
    while True:
        try:
            record = log_queue.get(timeout=5)
        except (queue.Empty, KeyboardInterrupt):
            continue
        logger = logging.getLogger(record.name)
        logger.handle(record)

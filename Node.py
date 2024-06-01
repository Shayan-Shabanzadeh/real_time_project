import threading
from enum import Enum
from queue import Queue
from random import Random

from constant import SEED


class LAYER(Enum):
    CLOUD = 1
    FOG = 2
    EDGE = 3


class Node:
    rnd = Random()
    rnd.seed(SEED)
    NODES = []

    def __init__(self, layer: LAYER, cpu_frequency: float = None, x_coordinate: float = None,
                 y_coordinate: float = None):
        self.node_id = len(Node.NODES) + 1
        self.layer = layer
        self.processing_queue = []
        self.arrival_queue = Queue()
        self.simulated_time = 0
        self.timer_lock = threading.Lock()
        self.message_queue = Queue()
        self.cpu_frequency = cpu_frequency
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.process_queue_lock = threading.Lock()
        self.arrival_queue_lock = threading.Lock()
        self.network_lock = threading.Lock()
        self.message_queue_lock = threading.Lock()

    @staticmethod
    def generate_node_cpu_frequency(MIN_CPU_FREQUENCY, MAX_CPU_FREQUENCY):
        return Node.rnd.uniform(MIN_CPU_FREQUENCY, MAX_CPU_FREQUENCY)

    def start(self):
        pass

    def get_task_with_min_deadline(self):
        if not self.processing_queue:
            return None
        min_deadline_task = min(self.processing_queue, key=lambda task: task.deadline)
        self.processing_queue.remove(min_deadline_task)
        return min_deadline_task

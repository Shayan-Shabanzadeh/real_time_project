from random import Random

import constant
from Node import Node, LAYER
from constant import SEED


class CloudNode(Node):
    rnd = Random()
    rnd.seed(SEED)
    CLOUD_NODES = []

    def __init__(self, node_id, cpu_frequency, x_coordinate=None, y_coordinate=None):
        super().__init__(node_id, LAYER.CLOUD, cpu_frequency, x_coordinate, y_coordinate)

    def __str__(self):
        return (f"CloudNode(ID: {self.node_id}, "
                f"CPU Frequency: {self.cpu_frequency} GHz, "
                f"Coordinates: ({self.x_coordinate}, {self.y_coordinate}), "
                f"Processing Queue Size: {self.processing_queue.qsize()}, "
                f"Message Queue Size: {self.message_queue.qsize()})")

    @staticmethod
    def generate_cloud_nodes():
        count = constant.NUMBER_OF_CLOUD_NODES
        min_cpu_frequency = constant.MIN_CLOUD_CPU_FREQUENCY
        max_cpu_frequency = constant.MAX_CLOUD_CPU_FREQUENCY
        CloudNode.CLOUD_NODES.clear()
        for i in range(count):
            cpu_frequency = CloudNode.generate_node_cpu_frequency(min_cpu_frequency, max_cpu_frequency)
            node = CloudNode(node_id=i, cpu_frequency=cpu_frequency)
            CloudNode.CLOUD_NODES.append(node)

    @staticmethod
    def generate_node_cpu_frequency(MIN_CPU_FREQUENCY, MAX_CPU_FREQUENCY):
        return CloudNode.rnd.uniform(MIN_CPU_FREQUENCY, MAX_CPU_FREQUENCY)
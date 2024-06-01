from random import Random

import constant
from Node import Node, LAYER
from constant import SEED


class FogNode(Node):
    rnd = Random()
    rnd.seed(SEED)
    FOG_NODES = []

    def __init__(self, node_id, cpu_frequency, x_coordinate=None, y_coordinate=None):
        super().__init__(node_id, LAYER.FOG, cpu_frequency, x_coordinate, y_coordinate)

    def __str__(self):
        return (f"FogNode(ID: {self.node_id}, "
                f"CPU Frequency: {self.cpu_frequency} GHz, "
                f"Coordinates: ({self.x_coordinate}, {self.y_coordinate}), "
                f"Processing Queue Size: {self.processing_queue.qsize()}, "
                f"Message Queue Size: {self.message_queue.qsize()})")

    @staticmethod
    def generate_fog_nodes():
        count = constant.NUMBER_OF_FOG_NODES
        min_cpu_frequency = constant.MIN_FOG_CPU_FREQUENCY
        max_cpu_frequency = constant.MAX_FOG_CPU_FREQUENCY
        FogNode.FOG_NODES.clear()
        for i in range(count):
            cpu_frequency = FogNode.generate_node_cpu_frequency(min_cpu_frequency, max_cpu_frequency)
            node = FogNode(node_id=i, cpu_frequency=cpu_frequency)
            FogNode.FOG_NODES.append(node)

    @staticmethod
    def generate_node_cpu_frequency(MIN_CPU_FREQUENCY, MAX_CPU_FREQUENCY):
        return FogNode.rnd.uniform(MIN_CPU_FREQUENCY, MAX_CPU_FREQUENCY)

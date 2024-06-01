import threading
import time
from random import Random

import constant
from Node import Node, LAYER
from constant import SEED


class FogNode(Node):
    rnd = Random()
    rnd.seed(SEED)
    FOG_NODES = []

    def __init__(self, cpu_frequency, x_coordinate=None, y_coordinate=None):
        super().__init__(LAYER.FOG, cpu_frequency, x_coordinate, y_coordinate)

    def __str__(self):
        return (f"FogNode(ID: {self.node_id}, "
                f"CPU Frequency: {self.cpu_frequency} GHz, "
                f"Coordinates: ({self.x_coordinate}, {self.y_coordinate}), "
                f"Processing Queue Size: {len(self.processing_queue)}, "
                f"Message Queue Size: {self.message_queue.qsize()}), "
                f"x_coordinate: {self.x_coordinate}, "
                f"y_coordinate: {self.y_coordinate}")

    @staticmethod
    def generate_fog_nodes():
        count = constant.NUMBER_OF_FOG_NODES
        min_cpu_frequency = constant.MIN_FOG_CPU_FREQUENCY
        max_cpu_frequency = constant.MAX_FOG_CPU_FREQUENCY
        FogNode.FOG_NODES.clear()
        for i in range(count):
            cpu_frequency = FogNode.generate_node_cpu_frequency(min_cpu_frequency, max_cpu_frequency)
            node = FogNode(cpu_frequency=cpu_frequency)
            FogNode.FOG_NODES.append(node)
            Node.NODES.append(node)

    @staticmethod
    def generate_node_cpu_frequency(MIN_CPU_FREQUENCY, MAX_CPU_FREQUENCY):
        return FogNode.rnd.uniform(MIN_CPU_FREQUENCY, MAX_CPU_FREQUENCY)

    def start(self):
        print(f'Starting fog node: {self.node_id}')
        process_thread = threading.Thread(target=self._process_queue_thread)
        process_thread.start()
        process_thread.join()

    def _process_queue_thread(self):
        while self.simulated_time <= constant.SIMULATION_TIME:
            with self.process_queue_lock:
                if len(self.processing_queue) != 0:
                    task = self.get_task_with_min_deadline()
                    self.simulated_time = task.arrival_to_layer
                    task.submission_time = task.arrival_to_layer
                    task.execute_start_time = self.simulated_time
                    processing_time = task.processing_requirements / self.cpu_frequency

                    task.execution_time = processing_time
                    self.simulated_time += task.execution_time
                    task.status = "done"
                    task.finish_time = self.simulated_time
                    # print("----------------------")
                    # print(f'Processing task {task.task_id} on node {self.node_id} with deadline {task.deadline}')
                    # print(task)
                    # print(f'Task {task.task_id} processed.')

            time.sleep(0.01)

    def _increase_timer(self, time_to_simulate):
        if self.simulated_time <= constant.SIMULATION_TIME:
            with self.timer_lock:
                self.simulated_time += time_to_simulate
            # time.sleep(time_to_simulate)
        else:
            print("simulation is over.")
            SystemExit()

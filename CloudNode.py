import threading
import time
from random import Random

import constant
from Node import Node, LAYER
from constant import SEED


class CloudNode(Node):
    rnd = Random()
    rnd.seed(SEED)
    CLOUD_NODES = []

    def __init__(self, cpu_frequency, x_coordinate=None, y_coordinate=None):
        super().__init__(LAYER.CLOUD, cpu_frequency, x_coordinate, y_coordinate)

    def __str__(self):
        return (f"CloudNode(ID: {self.node_id}, "
                f"CPU Frequency: {self.cpu_frequency} GHz, "
                f"Coordinates: ({self.x_coordinate}, {self.y_coordinate}), "
                f"Processing Queue Size: {len(self.processing_queue)}, "
                f"Message Queue Size: {self.message_queue.qsize()}), "
                f"x_coordinate: {self.x_coordinate}, "
                f"y_coordinate: {self.y_coordinate}")

    @staticmethod
    def generate_cloud_nodes():
        count = constant.NUMBER_OF_CLOUD_NODES
        min_cpu_frequency = constant.MIN_CLOUD_CPU_FREQUENCY
        max_cpu_frequency = constant.MAX_CLOUD_CPU_FREQUENCY
        CloudNode.CLOUD_NODES.clear()
        for i in range(count):
            cpu_frequency = CloudNode.generate_node_cpu_frequency(min_cpu_frequency, max_cpu_frequency)
            node = CloudNode(cpu_frequency=cpu_frequency)
            CloudNode.CLOUD_NODES.append(node)
            Node.NODES.append(node)

    @staticmethod
    def generate_node_cpu_frequency(MIN_CPU_FREQUENCY, MAX_CPU_FREQUENCY):
        return CloudNode.rnd.uniform(MIN_CPU_FREQUENCY, MAX_CPU_FREQUENCY)

    def start(self):
        print(f'Starting cloud node: {self.node_id}')
        process_thread = threading.Thread(target=self._process_queue_thread)
        process_thread.start()
        process_thread.join()

    def _process_queue_thread(self):
        execution_time = 0
        empty_queue_time = 0
        while execution_time <= constant.SIMULATION_TIME:
            with self.process_queue_lock:
                if len(self.processing_queue) != 0:
                    empty_queue_time = 0  # Reset the timer when a task is found
                    task = self.get_task_with_min_deadline()
                    if task.arrival_to_layer > execution_time:
                        execution_time = task.arrival_to_layer
                    task.execute_start_time = execution_time
                    processing_time = task.processing_requirements / self.cpu_frequency
                    task.execution_time = processing_time
                    task.finish_time = execution_time + processing_time
                    if task.finish_time > task.deadline:
                        task.status = "failed"
                        continue
                    execution_time += task.execution_time
                    task.status = "done"
                    task.finish_time = execution_time
                    print("----------------------")
                    print(f'Processing task {task.task_id} on node {self.node_id} with deadline {task.deadline}')
                    print(task)
                    print(f'Task {task.task_id} processed.')

                else:
                    empty_queue_time += 0.1
                    time.sleep(0.1)
                if empty_queue_time >= 1:  # Check if the queue has been empty for 3 seconds
                    break  # Exit the loop

    def _increase_timer(self, time_to_simulate):
        if self.simulated_time <= constant.SIMULATION_TIME:
            with self.timer_lock:
                self.simulated_time += time_to_simulate
            # time.sleep(time_to_simulate)
        else:
            print("simulation is over.")
            SystemExit()

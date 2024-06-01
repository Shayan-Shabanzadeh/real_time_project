import threading
import time
from random import Random

import constant
from Node import Node, LAYER
from TaskGenerator import TaskGenerator
from constant import SEED


class EdgeNode(Node):
    rnd = Random()
    rnd.seed(SEED)
    EDGE_NODES = []

    def __init__(self, cpu_frequency, x_coordinate=None, y_coordinate=None):
        super().__init__(LAYER.EDGE, cpu_frequency, x_coordinate, y_coordinate)

    def __str__(self):
        return (f"EdgeNode(ID: {self.node_id}, "
                f"CPU Frequency: {self.cpu_frequency} GHz, "
                f"Coordinates: ({self.x_coordinate}, {self.y_coordinate}), "
                f"Processing Queue Size: {len(self.processing_queue)}, "
                f"Message Queue Size: {self.message_queue.qsize()}), "
                f"x_coordinate: {self.x_coordinate}, "
                f"y_coordinate: {self.y_coordinate}")

    @staticmethod
    def generate_edge_nodes():
        count = constant.NUMBER_OF_EDGE_NODES
        min_cpu_frequency = constant.MIN_EDGE_CPU_FREQUENCY
        max_cpu_frequency = constant.MAX_EDGE_CPU_FREQUENCY
        EdgeNode.EDGE_NODES.clear()
        for i in range(count):
            cpu_frequency = EdgeNode.generate_node_cpu_frequency(min_cpu_frequency, max_cpu_frequency)
            node = EdgeNode(cpu_frequency=cpu_frequency)
            EdgeNode.EDGE_NODES.append(node)
            Node.NODES.append(node)

    @staticmethod
    def generate_node_cpu_frequency(MIN_CPU_FREQUENCY, MAX_CPU_FREQUENCY):
        return EdgeNode.rnd.uniform(MIN_CPU_FREQUENCY, MAX_CPU_FREQUENCY)

    def start(self):
        print(f'Starting edge node: {self.node_id}')
        tasks = TaskGenerator.generate_tasks(avg_arrival_rate=constant.AVG_TASK_ARRIVAL_RATE)
        print(f'Generated: {len(tasks)} tasks')
        self._generate_arrival_queue(arrival_tasks=tasks)
        arrival_thread = threading.Thread(target=self._arrival_task_thread)
        process_thread = threading.Thread(target=self._process_queue_thread)
        arrival_thread.start()
        process_thread.start()
        arrival_thread.join()
        process_thread.join()

    def _generate_arrival_queue(self, arrival_tasks):
        for task in arrival_tasks:
            with self.arrival_queue_lock:  # Acquire the lock before accessing the queue
                task.node = self.node_id
                self.arrival_queue.put(task)

    def _arrival_task_thread(self):
        while self.simulated_time <= constant.SIMULATION_TIME:
            with self.arrival_queue_lock:  # Acquire the lock before accessing the queue
                if not self.arrival_queue.empty():
                    arrival_task = self.arrival_queue.get()
                    if arrival_task.arrival_time > self.simulated_time:
                        self._increase_timer(arrival_task.arrival_time - self.simulated_time)
                        if constant.SIMULATION_TYPE == "Local Only":
                            arrival_task.submission_time = arrival_task.arrival_time
                            with self.process_queue_lock:
                                self.processing_queue.append(arrival_task)
                        else:
                            pass
                    # TODO
            time.sleep(0.001)

    def _process_queue_thread(self):
        execution_time = 0
        while self.simulated_time <= constant.SIMULATION_TIME:
            with self.process_queue_lock:
                if len(self.processing_queue) != 0:
                    task = self.get_task_with_min_deadline()
                    if task.submission_time > self.simulated_time:
                        self._increase_timer(task.submission_time - self.simulated_time)
                    if task.submission_time > execution_time:
                        execution_time = task.submission_time
                    task.execute_start_time = execution_time
                    processing_time = task.processing_requirements / self.cpu_frequency

                    task.execution_time = processing_time
                    execution_time += task.execution_time
                    task.status = "done"
                    task.finish_time = execution_time
                    print("----------------------")
                    print(f'Processing task {task.task_id} on node {self.node_id} with deadline {task.deadline}')
                    print(task)
                    print(f'Task {task.task_id} processed.')
                    if execution_time > self.simulated_time:
                        self._increase_timer(task.finish_time - self.simulated_time)
            time.sleep(0.01)

    def _increase_timer(self, time_to_simulate):
        if self.simulated_time <= constant.SIMULATION_TIME:
            with self.timer_lock:
                self.simulated_time += time_to_simulate
            # time.sleep(time_to_simulate)
        else:
            print("simulation is over.")
            SystemExit()

import threading
import time
from random import Random

import constant
from CloudNode import CloudNode
from FogNode import FogNode
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
        arrival_thread.join()
        process_thread.start()
        process_thread.join()

    def _generate_arrival_queue(self, arrival_tasks):
        for task in arrival_tasks:
            with self.arrival_queue_lock:  # Acquire the lock before accessing the queue
                task.node = self.node_id
                self.arrival_queue.put(task)

    def _arrival_task_thread(self):
        empty_queue_time = 0
        arrival_time = 0
        while arrival_time <= constant.SIMULATION_TIME:
            with self.arrival_queue_lock:  # Acquire the lock before accessing the queue
                if not self.arrival_queue.empty():
                    empty_queue_time = 0  # Reset the timer when a task is found
                    arrival_task = self.arrival_queue.get()
                    if arrival_task.arrival_time > arrival_time:
                        arrival_time = arrival_task.arrival_time
                        if constant.SIMULATION_TYPE == "Local Only":
                            arrival_task.submission_time = arrival_task.arrival_time
                            arrival_task.assigned_fog_node = self
                            with self.process_queue_lock:
                                self.processing_queue.append(arrival_task)
                        elif constant.SIMULATION_TYPE == "Fog Only":
                            from Link import Link
                            link, fog_node = Link.find_edge_fog_node(self)
                            link.simulate_send_message(arrival_task)
                            with fog_node.process_queue_lock:
                                arrival_task.assigned_fog_node = fog_node
                                arrival_task.has_offloaded = True
                                fog_node.processing_queue.append(arrival_task)
                        elif constant.SIMULATION_TYPE == "Cloud Only":
                            cloud_node = CloudNode.CLOUD_NODES[0]
                            from NetworkLayer import NetworkLayer
                            path = NetworkLayer.find_min_path(self, cloud_node)
                            offload_delay = sum(arrival_task.task_size / link.link_bandwidth for link in path)
                            arrival_task.arrival_to_layer += offload_delay
                            arrival_task.assigned_fog_node = cloud_node
                            arrival_task.has_offloaded = True
                            with cloud_node.process_queue_lock:
                                cloud_node.processing_queue.append(arrival_task)
                        elif constant.SIMULATION_TYPE == "Genetic Only":
                            best_node, offload_delay = self.genetic_algorithm(arrival_task)
                            arrival_task.assigned_fog_node = best_node
                            arrival_task.arrival_to_layer += offload_delay
                            if best_node is not self:
                                arrival_task.has_offloaded = True
                            with best_node.process_queue_lock:
                                best_node.processing_queue.append(arrival_task)
                                print(f'node with id {self.node_id} assigned task with id {arrival_task.task_id} '
                                      f'to node {best_node.node_id}')
                        else:
                            print("You died")
                else:
                    empty_queue_time += 0.1  # Increase the timer if the queue is empty

                if empty_queue_time >= 1:  # Check if the queue has been empty for 3 seconds
                    # print("Arrival queue has been empty for 1 seconds. Terminating thread.")
                    break  # Exit the loop

            time.sleep(0.01)

    def genetic_algorithm(self, task):
        population_size = 10
        generations = 20
        mutation_rate = 0.1

        def initialize_population():
            # Filter out only cloud and fog nodes and include this node itself
            valid_nodes = [node for node in Node.NODES if isinstance(node, (FogNode, CloudNode))]
            valid_nodes.append(self)
            return [self.rnd.choice(valid_nodes) for _ in range(population_size)]

        def fitness(node):
            processing_time = task.processing_requirements / node.cpu_frequency
            waiting_time = sum(t.processing_requirements for t in node.processing_queue) / node.cpu_frequency
            from NetworkLayer import NetworkLayer
            links = NetworkLayer.find_min_path(self, node)
            offload_delay = sum(task.task_size / link.link_bandwidth for link in links)
            return processing_time + waiting_time + offload_delay

        def select_parents(population):
            population.sort(key=fitness)
            return population[:2]

        def crossover(parent1, parent2):
            return self.rnd.choice([parent1, parent2])

        def mutate(node):
            if self.rnd.uniform(0, 1) < mutation_rate:
                valid_nodes = [node for node in Node.NODES if isinstance(node, (FogNode, CloudNode)) and node != self]
                return self.rnd.choice(valid_nodes)
            return node

        population = initialize_population()
        for _ in range(generations):
            new_population = []
            for _ in range(population_size):
                parents = select_parents(population)
                child = crossover(parents[0], parents[1])
                child = mutate(child)
                new_population.append(child)
            population = new_population

        best_node = min(population, key=fitness)
        from NetworkLayer import NetworkLayer
        links = NetworkLayer.find_min_path(self, best_node)
        offload_delay = sum(task.task_size / link.link_bandwidth for link in links)
        return best_node, offload_delay

    def _process_queue_thread(self):
        execution_time = 0
        empty_queue_time = 0
        while execution_time <= constant.SIMULATION_TIME:
            with self.process_queue_lock:
                if len(self.processing_queue) != 0:
                    empty_queue_time = 0  # Reset the timer when a task is found
                    task = self.get_task_with_min_deadline()
                    if task.submission_time > execution_time:
                        execution_time = task.submission_time
                    task.execute_start_time = execution_time
                    processing_time = task.processing_requirements / self.cpu_frequency
                    task.execution_time = processing_time
                    task.finish_time = execution_time + processing_time
                    if task.finish_time > task.deadline:
                        task.status = "failed"
                        continue
                    execution_time += task.execution_time
                    task.status = "done"

                    print("----------------------")
                    print(f'Processing task {task.task_id} on node {self.node_id} with deadline {task.deadline}')
                    print(task)
                    print(f'Task {task.task_id} processed.')

                else:
                    empty_queue_time += 0.1
                    time.sleep(0.01)
                if empty_queue_time >= 2:  # Check if the queue has been empty for 3 seconds
                    break  # Exit the loop

import threading
from random import Random

from Task import Task
from constant import *


class TaskGenerator:
    TASKS = []

    @staticmethod
    def generate_tasks(avg_arrival_rate: float):
        tasks = []
        current_time = 0.0
        rnd = Random()
        rnd.seed(SEED)

        def generate_single_task():
            nonlocal current_time
            task_arrival_time = 0
            while current_time < SIMULATION_TIME:
                # Generate inter-arrival time using Exponential distribution
                inter_arrival_time = rnd.expovariate(avg_arrival_rate)
                current_time += inter_arrival_time
                task_arrival_time += inter_arrival_time
                task_size = abs(rnd.normalvariate(task_size_mu, task_size_sigma))
                processing_requirements = abs(rnd.normalvariate(process_mu, process_sigma))
                network_communication_requirements = abs(rnd.normalvariate(process_mu, process_sigma))
                deadline = current_time + rnd.expovariate(deadline_lambda_parameter)

                # Create a new task
                task = Task(task_size=task_size, processing_requirements=processing_requirements,
                            submission_time=current_time, deadline=deadline,
                            network_communication_requirements=network_communication_requirements,
                            arrival_time=task_arrival_time, node=None)

                tasks.append(task)

        # Create and start a thread for task generation
        task_generation_thread = threading.Thread(target=generate_single_task)
        task_generation_thread.start()

        # Wait for the thread to finish
        task_generation_thread.join()
        TaskGenerator.TASKS.append(tasks)
        return tasks

import threading
from random import Random

from CloudNode import CloudNode
from FogNode import FogNode
from Task import Task
import matplotlib.pyplot as plt
from constant import *


class TaskGenerator:
    TASKS = []
    total_response_time = 0
    total_waiting_time = 0
    successful_tasks = 0
    failed_tasks = 0
    offloaded_tasks = 0
    total_tasks = 0
    response_times = []
    waiting_times = []
    edge_executed = 0
    fog_offloaded = 0
    cloud_offloaded = 0
    @staticmethod
    def generate_tasks(avg_arrival_rate: float):
        tasks = []
        current_time = 0.0
        rnd = Random()
        rnd.seed(SEED)

        def generate_single_task():
            nonlocal current_time
            task_arrival_time = 0
            while current_time < 30:
                # Generate inter-arrival time using Exponential distribution
                inter_arrival_time = rnd.expovariate(avg_arrival_rate)
                current_time += inter_arrival_time
                task_arrival_time += inter_arrival_time
                task_size = abs(rnd.normalvariate(task_size_mu, task_size_sigma))
                processing_requirements = abs(rnd.normalvariate(process_mu, process_sigma))
                network_communication_requirements = abs(rnd.normalvariate(process_mu, process_sigma))
                deadline = current_time + rnd.uniform(min_deadline, max_deadline)

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

    @staticmethod
    def print_statistics():
        total_response_time = 0
        total_waiting_time = 0
        successful_tasks = 0
        failed_tasks = 0
        offloaded_tasks = 0
        total_tasks = 0
        response_times = []
        waiting_times = []
        edge_executed = 0
        fog_offloaded = 0
        cloud_offloaded = 0

        for task_batch in TaskGenerator.TASKS:
            for task in task_batch:
                total_tasks += 1
                if task.status == "done":
                    response_time = task.finish_time - task.arrival_time
                    waiting_time = task.execute_start_time - task.submission_time
                    response_times.append(response_time)
                    waiting_times.append(waiting_time)
                    total_response_time += response_time
                    total_waiting_time += waiting_time
                    successful_tasks += 1

                    if isinstance(task.assigned_fog_node, FogNode):
                        fog_offloaded += 1
                    elif isinstance(task.assigned_fog_node, CloudNode):
                        cloud_offloaded += 1
                    else:
                        edge_executed += 1

                elif task.status == "failed":
                    failed_tasks += 1
                if task.has_offloaded:
                    offloaded_tasks += 1

        avg_response_time = total_response_time / successful_tasks if successful_tasks > 0 else 0
        avg_waiting_time = total_waiting_time / successful_tasks if successful_tasks > 0 else 0

        print(f"Average Response Time: {avg_response_time:.2f} seconds")
        print(f"Number of Successful Tasks: {successful_tasks}")
        print(f"Number of Failed Tasks: {failed_tasks}")
        print(f"Number of Offloaded Tasks: {offloaded_tasks}")
        print(f"Total Number of Tasks: {total_tasks}")

        TaskGenerator.plot_qos_parameters(response_times, waiting_times, edge_executed, fog_offloaded, cloud_offloaded,
                                          successful_tasks, failed_tasks, offloaded_tasks, avg_response_time,
                                          avg_waiting_time)

    @staticmethod
    def plot_qos_parameters(response_times, waiting_times, edge_executed, fog_offloaded, cloud_offloaded,
                            successful_tasks, failed_tasks, offloaded_tasks, avg_response_time, avg_waiting_time):
        # Plot Response Time Distribution
        plt.figure(figsize=(14, 10))

        plt.subplot(2, 2, 1)
        plt.hist(response_times, bins=20, color='blue', edgecolor='black', alpha=0.7)
        plt.axvline(avg_response_time, color='r', linestyle='dashed', linewidth=1)
        plt.title('Response Time Distribution')
        plt.xlabel('Response Time (s)')
        plt.ylabel('Frequency')
        plt.text(avg_response_time * 1.1, max(plt.ylim()) * 0.9, f'Avg: {avg_response_time:.2f}', color='r')
        plt.xticks(rotation=45)

        # Plot Waiting Time Distribution
        plt.subplot(2, 2, 2)
        plt.hist(waiting_times, bins=20, color='orange', edgecolor='black', alpha=0.7)
        plt.axvline(avg_waiting_time, color='r', linestyle='dashed', linewidth=1)
        plt.title('Waiting Time Distribution')
        plt.xlabel('Waiting Time (s)')
        plt.ylabel('Frequency')
        plt.text(avg_waiting_time * 1.1, max(plt.ylim()) * 0.9, f'Avg: {avg_waiting_time:.2f}', color='r')
        plt.xticks(rotation=45)

        # Plot Number of Tasks by Execution Location
        plt.subplot(2, 2, 3)
        locations = ['Edge Executed', 'Fog Offloaded', 'Cloud Offloaded']
        values = [edge_executed, fog_offloaded, cloud_offloaded]
        bars = plt.bar(locations, values, color=['green', 'red', 'blue'])
        plt.title('Task Execution Locations')
        plt.ylabel('Number of Tasks')
        plt.xticks(rotation=45)
        for bar, value in zip(bars, values):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 5, str(value), ha='center', va='bottom')

        # Plot Task Completion Rates
        plt.subplot(2, 2, 4)
        statuses = ['Done', 'Failed', 'Offloaded']
        counts = [successful_tasks, failed_tasks, offloaded_tasks]
        bars = plt.bar(statuses, counts, color=['green', 'red', 'orange'])
        plt.title('Task Completion Counts')
        plt.ylabel('Number of Tasks')
        plt.xticks(rotation=45)
        for bar, count in zip(bars, counts):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 5, f'{count}', ha='center', va='bottom')
        plt.tight_layout()
        plt.show()


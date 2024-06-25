import uuid


class Task:

    def __init__(self, task_size: float, processing_requirements: float, submission_time: float,
                 deadline: float, network_communication_requirements: float, arrival_time: float, node):
        self.task_id = uuid.uuid4()
        self.task_size = task_size
        # processing requirement is cpu frequency in Ghz
        self.processing_requirements = processing_requirements
        self.submission_time = submission_time
        self.arrival_time = arrival_time
        self.execute_start_time = -1
        self.has_offloaded = False
        # network communication requirement is in MByte
        self.network_communication_requirements = network_communication_requirements
        self.deadline = deadline
        # "waiting", "in_progress", "completed", "failed", etc.
        self.status = "waiting"
        self.assigned_fog_node = None
        self.execution_time = None
        self.finish_time = -1
        self.result_data = None
        self.arrival_to_layer = self.arrival_time
        self.node = None

    def __str__(self):
        return (
            f"Task ID: {self.task_id}\n"
            f"Task Size: {self.task_size}MB\n"
            f"Processing Requirements: {self.processing_requirements}Ghz\n"
            f"Submission Time: {self.submission_time}s\n"
            f"Arrival Time: {self.arrival_time}s\n"
            f"Execute Start Time: {self.execute_start_time}s\n"
            f"Network Communication Requirements: {self.network_communication_requirements} MB\n"
            f"Deadline: {self.deadline}s\n"
            f"Status: {self.status}\n"
            f"Assigned Fog Node: {self.assigned_fog_node}\n"
            f"Execution Time: {self.execution_time}s\n"
            f"Finish Time: {self.finish_time}s\n"
            f"Start Execute Time: {self.execute_start_time}s\n"
            f"Result Data: {self.result_data}\n"
            f"Arrival To Layer: {self.arrival_to_layer}"
        )

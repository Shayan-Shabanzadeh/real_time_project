import threading
from enum import Enum
from random import Random

import constant
from EdgeNode import EdgeNode
from FogNode import FogNode
from Node import Node, LAYER
from Task import Task
from constant import SEED


class LINK_TYPE(Enum):
    EDGE_FOG = 1
    FOG_CLOUD = 2
    FOG_FOG = 3


class Link:
    rnd = Random()
    rnd.seed(SEED)
    LINKS = []
    probability_connect_nodes = constant.PROBILITY_CONNECT_NODES
    connected_pairs = set()

    def __init__(self, link_id, node1: Node, node2: Node, link_type: LINK_TYPE):
        self.link_id = link_id
        self.node1 = node1
        self.node2 = node2
        self.link_type = link_type
        self.link_bandwidth = self.calculate_link_bandwidth()
        self.lock = threading.Lock()

    def calculate_link_bandwidth(self):
        max_bandwidth = 0
        min_bandwidth = 0
        if self.link_type is LINK_TYPE.FOG_FOG:
            max_bandwidth = constant.FOG_MAX_LINK_BANDWIDTH
            min_bandwidth = constant.EDGE_MIN_LINK_BANDWIDTH
        elif self.link_type is LINK_TYPE.EDGE_FOG:
            max_bandwidth = constant.EDGE_MAX_LINK_BANDWIDTH
            min_bandwidth = constant.EDGE_MIN_LINK_BANDWIDTH
        elif self.link_type is LINK_TYPE.FOG_CLOUD:
            max_bandwidth = constant.CLOUD_MAX_LINK_BANDWIDTH
            min_bandwidth = constant.CLOUD_MIN_LINK_BANDWIDTH

        return Link.rnd.uniform(min_bandwidth, max_bandwidth)

    @staticmethod
    def generate_links(cloud_nodes, edge_nodes, fog_nodes):
        Link.LINKS.clear()
        link_id = 0

        # Connect cloud nodes in a chain
        for i in range(len(cloud_nodes) - 1):
            link = Link(link_id, cloud_nodes[i], cloud_nodes[i + 1], LINK_TYPE.FOG_CLOUD)
            Link.LINKS.append(link)
            Link.connected_pairs.add((cloud_nodes[i], cloud_nodes[i + 1]))
            link_id += 1

        # Connect each fog node to at least one cloud node
        for fog_node in fog_nodes:
            cloud_node = Link.rnd.choice(cloud_nodes)
            link = Link(link_id, fog_node, cloud_node, LINK_TYPE.FOG_CLOUD)
            Link.LINKS.append(link)
            Link.connected_pairs.add((fog_node, cloud_node))
            link_id += 1

        for edge_node in edge_nodes:
            fog_node = Link.rnd.choice(fog_nodes)
            link = Link(link_id, edge_node, fog_node, LINK_TYPE.EDGE_FOG)
            Link.LINKS.append(link)
            Link.connected_pairs.add((edge_node, fog_node))
            link_id += 1

        # Additional connections based on probability
        all_nodes = cloud_nodes + fog_nodes + edge_nodes
        for node1 in all_nodes:
            for node2 in all_nodes:
                if node1 != node2 and (node1, node2) not in Link.connected_pairs:
                    if isinstance(node1, Node) and isinstance(node2, Node):
                        if Link.rnd.random() < Link.probability_connect_nodes:
                            if node1.layer == LAYER.FOG and node2.layer == LAYER.CLOUD:
                                link_type = LINK_TYPE.FOG_CLOUD
                            elif node1.layer == LAYER.EDGE and node2.layer == LAYER.FOG:
                                link_type = LINK_TYPE.EDGE_FOG
                            elif node1.layer == LAYER.FOG and node2.layer == LAYER.FOG:
                                link_type = LINK_TYPE.FOG_FOG
                            else:
                                continue
                            link = Link(link_id, node1, node2, link_type)
                            Link.LINKS.append(link)
                            Link.connected_pairs.add((node1, node2))
                            link_id += 1

    @staticmethod
    def find_link(node1, node2):
        for link in Link.LINKS:
            if (link.node1 == node1 and link.node2 == node2) or (link.node1 == node2 and link.node2 == node1):
                return link
        return None

    # assume ever edge node is only connected to one fog node
    @staticmethod
    def find_edge_fog_node(node1: EdgeNode):
        for link in Link.LINKS:
            if link.node1 is node1:
                if link.node2.layer is LAYER.FOG:
                    return link, link.node2
            elif link.node2 is node1:
                if link.node1.layer is LAYER.FOG:
                    return link, link.node1
            else:
                continue

    @staticmethod
    def find_fog_to_cloud_link(fog_node: FogNode):
        for link in Link.LINKS:
            if link.node1 is fog_node:
                if link.node2.layer is LAYER.CLOUD:
                    return link, link.node2
            elif link.node2 is fog_node:
                if link.node1.layer is LAYER.CLOUD:
                    return link, link.node1
            else:
                continue

    def simulate_send_message(self, task: Task):
        with self.lock:
            interarrival_time = task.task_size / self.link_bandwidth
            task.arrival_to_layer += interarrival_time

    def __str__(self):
        return (f"Link(ID: {self.link_id}, "
                f"Node1: {self.node1.node_id} ({self.node1.layer.name}), "
                f"Node2: {self.node2.node_id} ({self.node2.layer.name}), "
                f"Type: {self.link_type.name}, "
                f"Bandwidth: {self.link_bandwidth:.2f} Gbps)")

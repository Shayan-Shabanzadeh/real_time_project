import math
import threading
from random import Random

import networkx as nx
from matplotlib import pyplot as plt

import constant
from CloudNode import CloudNode
from EdgeNode import EdgeNode
from FogNode import FogNode
from Link import Link, LINK_TYPE
from Node import LAYER

# Constants
city_width = constant.city_weight  # 1000m
city_height = constant.city_height  # 1000m
min_distance_between_cloud_nodes = constant.min_distance_between_cloud_nodes  # 100m

max_distance_between_fog_to_cloud = constant.max_distance_between_fog_to_cloud
min_distance_between_fog_to_cloud = constant.min_distance_between_fog_to_cloud

max_distance_between_fog_to_fog = constant.max_distance_between_fog_to_fog
min_distance_between_fog_to_fog = constant.min_distance_between_fog_to_fog

max_distance_between_edge_to_fog = constant.max_distance_between_edge_to_fog
min_distance_between_edge_to_fog = constant.min_distance_between_edge_to_fog

random = Random()
random.seed(constant.SEED)


class NetworkLayer:
    def __init__(self):
        FogNode.generate_fog_nodes()
        CloudNode.generate_cloud_nodes()
        EdgeNode.generate_edge_nodes()
        Link.generate_links(fog_nodes=FogNode.FOG_NODES,
                            cloud_nodes=CloudNode.CLOUD_NODES,
                            edge_nodes=EdgeNode.EDGE_NODES)
        self.fog_nodes = FogNode.FOG_NODES
        self.cloud_nodes = CloudNode.CLOUD_NODES
        self.edge_nodes = EdgeNode.EDGE_NODES
        self.nodes = self.fog_nodes + self.cloud_nodes + self.edge_nodes
        self.links = Link.LINKS
        NetworkLayer.assign_coordinates_to_nodes(cloud_nodes=self.cloud_nodes,
                                                 fog_nodes=self.fog_nodes,
                                                 edge_nodes=self.edge_nodes)

        # Debugging print statements to check lengths
        print(f"Number of fog nodes: {len(self.fog_nodes)}")
        print(f"Number of cloud nodes: {len(self.cloud_nodes)}")
        print(f"Number of edge nodes: {len(self.edge_nodes)}")
        print(f"Total number of nodes: {len(self.nodes)}")

    @staticmethod
    def distance(x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    @staticmethod
    def assign_coordinates_to_nodes(cloud_nodes, fog_nodes, edge_nodes):
        # Assign coordinates to cloud nodes
        for i, cloud_node in enumerate(cloud_nodes):
            while True:
                x = random.uniform(0, city_width)
                y = random.uniform(0, city_height)
                if all(NetworkLayer.distance(x, y, other.x_coordinate, other.y_coordinate)
                       >= min_distance_between_cloud_nodes
                       for other in cloud_nodes[:i]):
                    cloud_node.x_coordinate = x
                    cloud_node.y_coordinate = y
                    break

        # Assign coordinates to fog nodes
        for fog_node in fog_nodes:
            connected_clouds = [link.node2 for link in Link.LINKS if
                                link.node1 == fog_node and link.link_type == LINK_TYPE.FOG_CLOUD] + \
                               [link.node1 for link in Link.LINKS if
                                link.node2 == fog_node and link.link_type == LINK_TYPE.FOG_CLOUD]
            while True:
                valid_position = True
                x = random.uniform(0, city_width)
                y = random.uniform(0, city_height)
                for cloud_node in connected_clouds:
                    dist = NetworkLayer.distance(x, y, cloud_node.x_coordinate, cloud_node.y_coordinate)
                    if not (min_distance_between_fog_to_cloud <= dist <= max_distance_between_fog_to_cloud):
                        valid_position = False
                        break
                if valid_position:
                    fog_node.x_coordinate = x
                    fog_node.y_coordinate = y
                    break

        # Assign coordinates to edge nodes
        for edge_node in edge_nodes:
            connected_fogs = [link.node2 for link in Link.LINKS if
                              link.node1 == edge_node and link.link_type == LINK_TYPE.EDGE_FOG] + \
                             [link.node1 for link in Link.LINKS if
                              link.node2 == edge_node and link.link_type == LINK_TYPE.EDGE_FOG]
            while True:
                valid_position = True
                x = random.uniform(0, city_width)
                y = random.uniform(0, city_height)
                for fog_node in connected_fogs:
                    dist = NetworkLayer.distance(x, y, fog_node.x_coordinate, fog_node.y_coordinate)
                    if not (min_distance_between_edge_to_fog <= dist <= max_distance_between_edge_to_fog):
                        valid_position = False
                        break
                if valid_position:
                    edge_node.x_coordinate = x
                    edge_node.y_coordinate = y
                    break

        # Check and adjust distances between fog nodes
        for fog_node in fog_nodes:
            connected_fogs = [link.node2 for link in Link.LINKS if
                              link.node1 == fog_node and link.link_type == LINK_TYPE.FOG_FOG] + \
                             [link.node1 for link in Link.LINKS if
                              link.node2 == fog_node and link.link_type == LINK_TYPE.FOG_FOG]
            while True:
                valid_position = True
                for other_fog_node in connected_fogs:
                    dist = NetworkLayer.distance(fog_node.x_coordinate, fog_node.y_coordinate,
                                                 other_fog_node.x_coordinate,
                                                 other_fog_node.y_coordinate)
                    if not (min_distance_between_fog_to_fog <= dist <= max_distance_between_fog_to_fog):
                        valid_position = False
                        break
                if valid_position:
                    break
                # Adjust position if necessary
                x = random.uniform(0, city_width)
                y = random.uniform(0, city_height)
                fog_node.x_coordinate = x
                fog_node.y_coordinate = y

    def create_topology_graph(self):
        G = nx.Graph()
        for link in self.links:
            G.add_edge(link.node1.node_id, link.node2.node_id, bandwidth=link.link_bandwidth, link_object=link)
        return G

    def visualize_topology(self):
        G = self.create_topology_graph()
        pos = {node.node_id: (node.x_coordinate, node.y_coordinate) for node in self.nodes}

        # Ensure all nodes have been assigned a position
        for node in self.nodes:
            if node.node_id not in pos:
                print(f"Node {node.node_id} has no position assigned.")

        # Define node colors based on layer
        node_colors = ["orange" if node.layer is LAYER.CLOUD else
                       "skyblue" if node.layer is LAYER.FOG else
                       "green" if node.layer is LAYER.EDGE else
                       "yellow" for node in self.nodes]

        labels = {node.node_id: f"{node.layer.name.capitalize()} {node.node_id}" for node in self.nodes}
        nx.draw(G, pos, with_labels=True, labels=labels, node_size=700, node_color=node_colors, font_size=8,
                font_color="black", font_weight="bold", edge_color="gray", width=2)

        plt.show()

    def start_simulation(self):
        threads = []
        for node in self.cloud_nodes:
            thread = threading.Thread(target=node.start)
            thread.start()
            threads.append(thread)
        for node in self.fog_nodes:
            thread = threading.Thread(target=node.start)
            thread.start()
            threads.append(thread)
        for node in self.edge_nodes:
            thread = threading.Thread(target=node.start)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()



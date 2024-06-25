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

    @staticmethod
    def create_topology_graph():
        G = nx.Graph()
        for link in Link.LINKS:
            G.add_edge(link.node1.node_id, link.node2.node_id, bandwidth=link.link_bandwidth, link_object=link)
        return G

    @staticmethod
    def find_min_path(start_node, end_node):
        G = NetworkLayer.create_topology_graph()
        try:
            shortest_path = nx.shortest_path(G, source=start_node.node_id, target=end_node.node_id, weight='bandwidth')
            path_links = []
            for i in range(len(shortest_path) - 1):
                node1 = shortest_path[i]
                node2 = shortest_path[i + 1]
                link = G[node1][node2]['link_object']
                path_links.append(link)
            return path_links
        except nx.NetworkXNoPath:
            return None

    @staticmethod
    def visualize_topology():
        G = NetworkLayer.create_topology_graph()
        from Node import Node
        pos = {node.node_id: (node.x_coordinate, node.y_coordinate) for node in Node.NODES}

        # Define node colors based on layer with additional debug prints
        node_colors = []
        for node in Node.NODES:
            if isinstance(node, CloudNode):
                node_colors.append("skyblue")
            elif isinstance(node, FogNode):
                node_colors.append("skyblue")
            elif isinstance(node, EdgeNode):
                node_colors.append("skyblue")
            else:
                node_colors.append("yellow")

        labels = {node.node_id: f"{node.layer.name.capitalize()} {node.node_id}" for node in Node.NODES}
        nx.draw(G, pos, with_labels=True, labels=labels, node_size=700, node_color=node_colors, font_size=8,
                font_color="black", font_weight="bold", edge_color="gray", width=2)

        plt.show()

    def start_simulation(self):
        edge_threads = []
        fog_threads = []
        cloud_thread = []
        for node in self.edge_nodes:
            thread = threading.Thread(target=node.start)
            thread.start()
            edge_threads.append(thread)
        for thread in edge_threads:
            thread.join()

        for node in self.fog_nodes:
            thread = threading.Thread(target=node.start)
            thread.start()
            fog_threads.append(thread)
        for thread in fog_threads:
            thread.join()
        for node in self.cloud_nodes:
            thread = threading.Thread(target=node.start)
            thread.start()
            cloud_thread.append(thread)
        for thread in cloud_thread:
            thread.join()

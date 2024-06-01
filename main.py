from CloudNode import CloudNode
from EdgeNode import EdgeNode
from FogNode import FogNode
from Link import Link

if __name__ == '__main__':
    FogNode.generate_fog_nodes()
    CloudNode.generate_cloud_nodes()
    EdgeNode.generate_edge_nodes()
    Link.generate_links(fog_nodes=FogNode.FOG_NODES,
                        cloud_nodes=CloudNode.CLOUD_NODES,
                        edge_nodes=EdgeNode.EDGE_NODES)
    for link in Link.LINKS:
        print(link)
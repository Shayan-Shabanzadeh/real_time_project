from FogNode import FogNode
from Node import LAYER, Node

if __name__ == '__main__':
    FogNode.generate_fog_nodes()
    for node in FogNode.FOG_NODES:
        print(node)

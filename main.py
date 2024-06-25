from NetworkLayer import NetworkLayer
from TaskGenerator import TaskGenerator

if __name__ == '__main__':
    network_layer = NetworkLayer()
    network_layer.visualize_topology()
    network_layer.start_simulation()
    TaskGenerator.print_statistics()


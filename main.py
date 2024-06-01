from NetworkLayer import NetworkLayer

if __name__ == '__main__':
    network_layer = NetworkLayer()
    for node in network_layer.nodes:
        print(node)
    network_layer.start_simulation()

    # network_layer.visualize_topology()
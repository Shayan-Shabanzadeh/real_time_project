SIMULATION_TIME = 600
SIMULATION_TYPE = "Local Only"
SEED = 1234
NUMBER_OF_FOG_NODES = 1
NUMBER_OF_EDGE_NODES = 1
NUMBER_OF_CLOUD_NODES = 1

AVG_TASK_ARRIVAL_RATE = 10

MAX_EDGE_CPU_FREQUENCY = 1.5
MIN_EDGE_CPU_FREQUENCY = 0.5

MAX_FOG_CPU_FREQUENCY = 2.5
MIN_FOG_CPU_FREQUENCY = 1.6

MAX_CLOUD_CPU_FREQUENCY = 3.5
MIN_CLOUD_CPU_FREQUENCY = 2.6

EDGE_MAX_LINK_BANDWIDTH = 200
EDGE_MIN_LINK_BANDWIDTH = 100

FOG_MAX_LINK_BANDWIDTH = 99
FOG_MIN_LINK_BANDWIDTH = 50

CLOUD_MAX_LINK_BANDWIDTH = 50
CLOUD_MIN_LINK_BANDWIDTH = 3

PROBILITY_CONNECT_NODES = 0.3

city_weight = 1000  # 1000m
city_height = 1000  # 1000m
min_distance_between_cloud_nodes = 100  # 100m

max_distance_between_fog_to_cloud = 100
min_distance_between_fog_to_cloud = 40

max_distance_between_fog_to_fog = 100
min_distance_between_fog_to_fog = 40

max_distance_between_edge_to_fog = 50
min_distance_between_edge_to_fog = 10

task_size_mu = 3
task_size_sigma = 10

process_mu = 10
process_sigma = 20

network_communication_mu = 10
network_communication_sigma = 20

deadline_lambda_parameter = 0.1

ctrl_message_mu = 0.01
ctrl_message_sigma = 0.01

SIMULATION_TIME = 60
SIMULATION_TYPE = "Cloud Only"
SEED = 1234
NUMBER_OF_FOG_NODES = 1
NUMBER_OF_EDGE_NODES = 1
NUMBER_OF_CLOUD_NODES = 1

AVG_TASK_ARRIVAL_RATE = 2

MAX_EDGE_CPU_FREQUENCY = 1.5
MIN_EDGE_CPU_FREQUENCY = 0.5

MAX_FOG_CPU_FREQUENCY = 2.5
MIN_FOG_CPU_FREQUENCY = 1.6

MAX_CLOUD_CPU_FREQUENCY = 20
MIN_CLOUD_CPU_FREQUENCY = 10

EDGE_MAX_LINK_BANDWIDTH = 10
EDGE_MIN_LINK_BANDWIDTH = 6

FOG_MAX_LINK_BANDWIDTH = 5
FOG_MIN_LINK_BANDWIDTH = 4

CLOUD_MAX_LINK_BANDWIDTH = 3
CLOUD_MIN_LINK_BANDWIDTH = 1

PROBILITY_CONNECT_NODES = 0.0

city_weight = 1000  # 1000m
city_height = 1000  # 1000m
min_distance_between_cloud_nodes = 100  # 100m

max_distance_between_fog_to_cloud = 100
min_distance_between_fog_to_cloud = 40

max_distance_between_fog_to_fog = 100
min_distance_between_fog_to_fog = 40

max_distance_between_edge_to_fog = 50
min_distance_between_edge_to_fog = 10

task_size_mu = 15
task_size_sigma = 10

process_mu = 10
process_sigma = 20

network_communication_mu = 10
network_communication_sigma = 20

deadline_lambda_parameter = 0.1

ctrl_message_mu = 0.01
ctrl_message_sigma = 0.01

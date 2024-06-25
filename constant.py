SIMULATION_TIME = 200
SIMULATION_TYPE = "Cloud Only"
SEED = 1234
NUMBER_OF_FOG_NODES = 5
NUMBER_OF_EDGE_NODES = 10
NUMBER_OF_CLOUD_NODES = 1

AVG_TASK_ARRIVAL_RATE = 1.5

MAX_EDGE_CPU_FREQUENCY = 1.5
MIN_EDGE_CPU_FREQUENCY = 0.5

MAX_FOG_CPU_FREQUENCY = 6.6
MIN_FOG_CPU_FREQUENCY = 5.5

MAX_CLOUD_CPU_FREQUENCY = 25
MIN_CLOUD_CPU_FREQUENCY = 15

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

task_size_mu = 0.05
task_size_sigma = 0.5

process_mu = 0.8
process_sigma = 1.2

network_communication_mu = 0.05
network_communication_sigma = 0.5

max_deadline = 11
min_deadline = 1
deadline_lambda_parameter = 0.1

ctrl_message_mu = 0.01
ctrl_message_sigma = 0.01

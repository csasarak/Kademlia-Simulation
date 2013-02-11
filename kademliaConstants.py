# Author: Christopher Sasarak

# This file contains constants for use by the Kademlia simulation

bit_string_size = 8
k_bucket_size = 10
initial_network_size = 1000
failure_probability = .09
lookup_alpha = 3 # The number of nodes for the lookup_node method to
                 # query at each step
maximum_RTT_time = 2000 # Milliseconds
timeout_time = 5000 # If a node fails to reply to a ping, this is the timeout time

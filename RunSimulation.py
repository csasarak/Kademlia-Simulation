#!/usr/bin/env python2.7
# Author: Christopher Sasarak
# This file contains code to run a simulation of the Kademlia system.

import sys
import node
from simulation import Simulation

usage = """Usage: ./RunSimulation.py <random seed> <network size> <trials> <disable frequency>
During each trial, the disable frequency is multiplied by the trial number to get the number of nodes to disable for that trial"""

if len(sys.argv) < 5:
    print usage
    sys.exit(1)

try:
    network_size = int(sys.argv[2])
    trials = int(sys.argv[3])
    seed = int(sys.argv[1])
    # The rate at which we will disable nodes 
    node_disable_n = int(sys.argv[4])
except ValueError:
    print usage
    sys.exit(1)

print "Building network"    
sim = Simulation(seed, network_size)
lookups = 1000
# Train the network a bit by doing random lookups
for i in range(3000):
    if i % 10 == 0:
        sys.stdout.write("\rInitializing network {0:.1f}%".format(i / 3000.0 * 100))
        sys.stdout.flush()
    sim.perform_node_lookup()
    
sys.stdout.write("\rInitializing network 100% \n\n")
sys.stdout.flush()

for n in sim.nodes:
    n.totalLookupDuration = 0

for trial in range(trials):
    print "================================================================================"
    sim.disable_nodes(trial * node_disable_n)
    
    print "\nTrial ", trial, " with ", trial * node_disable_n, " nodes disabled"

    # Perform lookups and then get the average time
    for i in range(lookups):
        sim.perform_node_lookup()

    time_sum = 0
    for n in sim.nodes:
        time_sum = time_sum + n.totalLookupDuration
        n.totalLookupDuration = 0

    print "Avg. lookup time: {0:.4f} seconds".format(time_sum / network_size/ 1000)

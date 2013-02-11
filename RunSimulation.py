#!/usr/bin/env python2.7
# Author: Christopher Sasarak
# This file contains code to run a simulation of the Kademlia system.

import sys
import node
from simulation import Simulation

if len(sys.argv) < 5:
    print """Usage: ./RunSimulation.py <random seed> <network size> <trials> <disable frequency>
During each trial, the disable frequency is multiplied by the trial number to get the number of nodes to disable for that trial"""
    sys.exit(1)

network_size = int(sys.argv[2])
trials = int(sys.argv[3])
seed = int(sys.argv[1])
lookups = 1000

# The rate at which we will disable nodes 
node_disable_n = int(sys.argv[4])
sim = Simulation(seed, network_size)


# Train the network a bit by doing random lookups
for i in range(3000):
    sim.perform_node_lookup()

for n in sim.nodes:
    n.totalLookupDuration = 0
    
start_state = sim.rand.getstate()    
for trial in range(trials):

    print "Trial ", trial, " with ", trial * node_disable_n, " nodes disabled"

    # Perform lookups and then get the average time
    for i in range(lookups):
        sim.perform_node_lookup()

    time_sum = 0
    for n in sim.nodes:
        time_sum = time_sum + n.totalLookupDuration
        n.totalLookupDuration = 0

    sim.disable_nodes(trial * node_disable_n)

    print "\t Avg. lookup time: ", (time_sum / network_size/ 1000)
    # Reset the generator to the original state
    # sim.rand.setstate(start_state)

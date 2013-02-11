#!/usr/bin/env python2.7
# Author: Christopher Sasarak
# This file contains code to run a simulation of the Kademlia system.

import sys
import node
from simulation import Simulation

if len(sys.argv) < 4:
    print "Usage: ./RunSimulation.py <random seed> <network size> <trials>"
    sys.exit(1)

network_size = int(sys.argv[2])
trials = int(sys.argv[3])
seed = int(sys.argv[1])
lookups = 1000

# The rate at which we will disable nodes 
node_disable_n = 5
sim = Simulation(seed, network_size)


# Train the network a bit by doing random lookups
for i in range(10000):
    sim.perform_node_lookup()

start_state = sim.rand.getstate()    
for trial in range(trials):

    print "Trial ", trial

    # Perform lookups and then get the average time
    for i in range(lookups):
        sim.perform_node_lookup()

    time_sum = 0
    for n in sim.nodes:
        time_sum = time_sum + n.totalHopDuration
        n.totalHopDuration = 0

    print "\t Avg. lookup time: ", (time_sum/ 1000)
    # Reset the generator to the original state
    # sim.rand.setstate(start_state)

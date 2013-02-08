#!/usr/bin/env python2.7
# Author: Christopher Sasarak
# This file contains code to run a simulation of the Kademlia system.

import sys
import node
from simulation import Simulation

if len(sys.argv) < 2:
    print "Usage: ./RunSimulation.py <random seed>"
    sys.exit(1)

seed = int(sys.argv[1])

sim = Simulation(seed)

print str(sim)


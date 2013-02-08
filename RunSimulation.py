#!/usr/bin/env python2.7
# Author: Christopher Sasarak
# This file contains code to run a simulation of the Kademlia system.

import Node
import sys
import random

if len(sys.argv) < 2:
    print "Usage: ./RunSimulation.py <random seed>"
    sys.exit(1)

random.seed(int(sys.argv[1]))



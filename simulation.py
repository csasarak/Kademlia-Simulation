# Author: Christopher Sasarak
# This file contains a simulation class. Simulation objects
# can be used to run different simulations

import random

import kademliaConstants
from node import Node


class Simulation:

    def __init__(self, seed, init_size=None):
        """
        This constructor will set up a Simulation object by populating it with
        an initial network.

        init_size -- Option parameter which defines an initial network size. If it
                     is not provided, then kademliaConstants.initial_network_size will be used.
        seed -- Seed the random number generator used by this Simulation
        """
        self.rand = random.Random()
        self.rand.seed(seed)
        
        self.init_size = init_size if init_size else kademliaConstants.initial_network_size

        self.build_network()

    def perform_node_lookup(self):
        """
        Perform a node lookup between two random nodes, return the
        time that it took to complete the lookup.
        """
        nodes = self.rand.sample(self.nodes, 2)

        target_node = nodes[1] 
        start_node = nodes[0]
        
        start_node.lookup_node(target_node.id)
        
        
        
    def build_network(self, n = None):
        """
        Build an initial network with, IDs are determined by a random
        function, and k-buckets are empty. Running this multiple times will replace the
        current network each time.

        n -- Optional parameter to set the initial size. If not provided, then it will use
             the size parameter set by the containing Simulation object.
        """
        size = n if n else self.init_size
        self.nodes = list()
        
        for i in range(0, size):
            new_node = Node(self.random_IP(), self.rand)
            
            # Select a random existing node if this isn't the first node,
            # then use it to perform a network join
            if not i == 0:
                contact_node = self.rand.choice(self.nodes)
                # Update new_node with the random contact node
                new_node.join_network(contact_node)
                
            self.nodes.append(new_node)
    
    def random_IP(self):
        """
        Generate a random IP address.

        returns a string representation of an IP address.
        """
        octets = list()

        for i in range(0, 4):
            octets.append(str(self.rand.randint(0, 255)))

        return ".".join(octets)
        
    def __str__(self):
        """
        Create a string representation of the simulation.

        """
        string = "Simulation: \n"
        
        for n in self.nodes:
            string = "{} {}\n".format(string, str(n))

        return string

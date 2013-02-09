# Author: Christopher Sasarak
import kademliaConstants
import math
import hashlib

class Node(object):
    """
    Implementation of a Kademlia node object.
    
    """
    
    def __init__(self, node_name, random):
        """
        Constructor for a Kademlia node.

        node_name -- The name (non-hashed) for this Node.
              Must be able to be represented as a bit-string with length < kademliaConstants.bit_string_size
              Generally this is an IP address.
        random -- A random number generator to use
        """
        self.node_name = node_name
        self.rand = random
        self.successor = None
        self.predecessor = None
        
        # Get the hash and truncate to the correct number of bits
        self.id = int(hashlib.sha1(self.node_name).hexdigest(), 16)
        self.id = self.id % int(math.pow(2, kademliaConstants.bit_string_size))
        
        self.kBuckets = list()
        self.key_value = (None, None)
        
        # Populate the Node with empty buckets
        for i in range(0, kademliaConstants.bit_string_size):
            self.kBuckets.append(KBucket(i, self, kademliaConstants.k_bucket_size))

    def update_kbuckets(func):
        """
        This decorator function will return a new function that
        updates a k-bucket with whatever node reference it was called with.

        func -- The function to decorate, normally this will be decorated with
        Python's annotation syntax.
        """
        def new_func(self, double):
            self.update_routing_table(double)
            func(double)

        return new_func
    
    @update_kbuckets
    def ping(self, _):
        """
        This method is used to test whether or not another node is
        still active. It randomly decides whether or not to send back
        a positive response using a factor defined in
        kademliaConstants.failure_probability.
        
        Return True if a response was received, False otherwise
        """ 
        if self.random.random() <= failure_probability:
            return False

        return True
    

    def update_routing_table(self, double):
        """
        Query update the routing table with 

        double -- A 2-tuple of the (ID, node reference) to look up in the routing table
        """
        ip, node_ref = double
        for k in self.kBuckets:
            if k.in_bucket(node_id):
                k.add_node(double)
                
    def compare_nodes(n1, n2):
        """
        Compare two nodes. Return a negative, positive, or zero if
        based on id n1 < n2, n1 > n2, or n1 == n2.

        n1 -- The first node for the comparison.
        n2 -- The second node for the comparison.
        """
        diff = n1.id - n2.id

        # Need to make this an integer, so check them
        if diff < 0:
            return -1
        elif diff > 0:
            return 1

        # We shouldn't get here if we're using a good enough hash function
        return 0
    
    def __str__(self):
        """
        Return a string representation of this Node and the contents of its k-buckets.
        """
        string = "Node {}, ID hash {}: ".format(self.node_name, hex(self.id))
        
        for i in self.kBuckets:
            string = "{} {}".format(string, str(i))

        return string

class KBucket(object):
    """
    This class represents a KBucket. Nodes keep a list of these to
    keep track of which nodes they have encountered.
    
    """
    
    class WrongKBucketException(Exception):
        """
        This exception is thrown when an attempt is made to add a double to a KBucket when that
        double is out of that KBucket's range.

        """
        pass
    
    def __init__(self, i, parent_node, k = None):
        """
        Constructor for the KBucket.

        i    -- The position of this KBucket in the Node's bucket-list
        node -- The node that this KBucket is referenced in.
        k    -- Optional, the size of the list of doubles this KBucket should maintain.
                If not included, then kademliaConstants.k_bucket_size will be used.
                
        """
        # Use default k size if none is provided
        if(k == None):
            self.k = KConstants.k_bucket_size
        else:
            self.k = k

        self.i = i
        self.node = parent_node
        self.doubles = list()


    def add_double(self, double):
        """
        Add a double comprised of a node ID and a reference to that node to this KBucket.

        double -- A 2-tuple of (node_id, node ref) to add to this KBucket

        WrongKBucketException -- Thrown if the given double's ID is not in this KBucket's space
        """
        node_id, node_ref  = double
        if(not self.in_bucket(node_id)):
            raise WrongKBucketException()
        
        ind = None

        try:
            index = self.doubles.index(double)
            t = self.doubles[index]
            self.doubles.delete(index)
            self.doubles.append(t)
        except ValueError:
            # Not in the k-bucket
            if(len(self.doubles) < self.k):
                self.doubles.append(double)
                return

            least_recently_seen = self.doubles[0]
            if(not self.node.ping(least_recently_seen)):
                self.doubles.delete(0)
                self.doubles.append(double)

            # k-bucket is full, throw away this double
                
                
    def in_bucket(self, other_id):
        """
        Determine if a particular ID goes into this kBucket.

        other_id -- The id to check against this KBucket's space
        """
        distance = self.node.id ^ other_id
        if(distance  <= math.pow(2, self.i+1) and distance > math.pow(2, self.i)):
            return True
        else:
            return False

    def __str__(self):
        """
        Return a string representation of this KBucket including the values of its doubles.
        
        """
        string = "\nkBucket {}: ".format(self.i)

        if(len(self.doubles) == 0):
            return "{} empty;".format(string)
        
        for b in self.doubles:
            ip, port, node_id = b
            string = "\n\t{} ({}, {}, {});".format(string, ip, port, hex(node_id) );

        return string

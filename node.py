# Author: Christopher Sasarak
import kademliaConstants
import math
import hashlib

class Node(object):
    """
    Implementation of a Kademlia node object.
    
    """
    
    def __init__(self, ID):
        """
        Constructor for a Kademlia node.

        ID -- The ID for this Node.
              Must be able to be represented as a bit-string with length < kademliaConstants.bit_string_size
              Generally this is an IP address.
        """
        self.id = ID
        self.successor = None
        self.predecessor = None
        
        # Get the hash and truncate to the correct number of bits
        self.id_hash = int(hashlib.sha1(self.id).hexdigest(), 16)
        self.id_hash = self.id_hash % int(math.pow(2, kademliaConstants.bit_string_size))
        
        self.kBuckets = list()
        self.key_value = (None, None)
        
        # Populate the Node with empty buckets
        for i in range(0, kademliaConstants.bit_string_size):
            self.kBuckets.append(KBucket(i, self, kademliaConstants.k_bucket_size))

    def ping(self, triple):
        """
        This method is used to test whether or not another node is active
        Return True if a response was received, False otherwise

        triple -- The triple to contact
        """ 
        return True

    def query(self, triple):
        """
        Query this node's routing table for a node, currently just adds the node to the table.

        triple -- A 3-tuple of the (IP, UDP Port, ID) to look up in the routing table
        
        """
        ip, port, node_id = triple
        for k in self.kBuckets:
            if k.in_bucket(node_id):
                try:
                    k.add_triple(triple)
                except WrongKBucketException:
                    pass

    def compare_nodes(n1, n2):
        """
        Compare two nodes. Return a negative, positive, or zero if
        based on id n1 < n2, n1 > n2, or n1 == n2.

        n1 -- The first node for the comparison.
        n2 -- The second node for the comparison.
        """
        diff = n1.id_hash - n2.id_hash

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
        string = "Node {}, ID hash {}: ".format(self.id, hex(self.id_hash))
        
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
        This exception is thrown when an attempt is made to add a triple to a KBucket when that
        triple is out of that KBucket's range.

        """
        pass
    
    def __init__(self, i, parent_node, k = None):
        """
        Constructor for the KBucket.

        i    -- The position of this KBucket in the Node's bucket-list
        node -- The node that this KBucket is referenced in.
        k    -- Optional, the size of the list of triples this KBucket should maintain.
                If not included, then kademliaConstants.k_bucket_size will be used.
                
        """
        # Use default k size if none is provided
        if(k == None):
            self.k = KConstants.k_bucket_size
        else:
            self.k = k

        self.i = i
        self.node = parent_node
        self.triples = list()


    def add_triple(self, triple ):
        """
        Add a triple to this KBucket.

        triple -- A 3-tuple of (IP, UDP Port, ID) to add to this KBucket

        WrongKBucketException -- Thrown if the given triple's ID is not in this KBucket's space
        
        """
        ip, port, node_id = triple
        if(not self.in_bucket(node_id)):
            raise WrongKBucketException()
        
        ind = None

        try:
            index = self.triples.index(triple)
            t = self.triples[index]
            self.triples.delete(index)
            self.triples.append(t)
        except ValueError:
            # Not in the k-bucket
            if(len(self.triples) < self.k):
                self.triples.append(triple)
                return

            least_recently_seen = self.triples[0]
            if(not self.node.ping(least_recently_seen)):
                self.triples.delete(0)
                self.triples.append(triple)

            # k-bucket is full, throw away this triple
                
                
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
        Return a string representation of this KBucket including the values of its triples.
        
        """
        string = "\nkBucket {}: ".format(self.i)

        if(len(self.triples) == 0):
            return "{} empty;".format(string)
        
        for b in self.triples:
            ip, port, node_id = b
            string = "\n\t{} ({}, {}, {});".format(string, ip, port, hex(node_id) );

        return string

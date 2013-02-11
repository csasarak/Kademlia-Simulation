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
        self.hopDuration = 0 # The collected duration for hops between
                             # this node and other nodes. The node
                             # calling the remote RPC is the one
                             # responsible for storing the RTT
        
        # Get the hash and truncate to the correct number of bits
        self.id = int(hashlib.sha1(self.node_name).hexdigest(), 16)
        self.id = self.id % int(math.pow(2, kademliaConstants.bit_string_size))
        
        self.kBuckets = list()
        self.data_table = dict()
        
        # Populate the Node with empty buckets
        for i in range(0, kademliaConstants.bit_string_size):
            self.kBuckets.append(KBucket(i, self, kademliaConstants.k_bucket_size))

    # THE RPCS FOR KADEMLIA ARE DEFINED HERE
    def ping(self, double):
        """
        This method is used to test whether or not another node is
        still active. It randomly decides whether or not to send back
        a positive response using a factor defined in
        kademliaConstants.failure_probability.
        
        Return True if a response was received, False otherwise
        """
        self.update_routing_table(double)
        if self.rand.random() <= kademliaConstants.failure_probability:
            return False

        return True

    def store(self, querying_node, key, value):
        """
        This RPC stores a key/value pair in this Node for later retrieval.

        querying_node -- A 2-tuple with a reference to the requesting node ID and the node reference
        key -- The key to store in this node
        value -- The value to associate with the key in this node
        """
        self.update_routing_table(querying_node) 
        self.data_table[key] = value

    def find_node(self, node_id, querying_node):
        """
        This RPC will search this nodes k-buckets for the k (as defined in kademliaConstants.k_bucket_size) closest nodes to the given node_id and return the list. There is a probability that this node will not be online, so return None if this is the case.

        node_id -- The node ID we are looking for nodes closest to
        querying_node -- A 2-tuple of the node id and a reference to
        the node of the node that called this RPC
        """
        if self.rand.random() <= kademliaConstants.failure_probability:
            return None
        
        self.update_routing_table(querying_node)

        # Find our closest bucket to the node_id
        closest = None
        for b in range(len(self.kBuckets)):
            if self.kBuckets[b].in_bucket(node_id):
                closest = b

        if len(self.kBuckets[b].doubles) > kademliaConstants.k_bucket_size:
            return self.kBuckets[b].doubles[0:kademliaConstants.k_bucket_size]

        # Other wise we must find at least k nodes closeby
        closest_list = list()
        closest_list.extend(self.kBuckets[b].doubles)
        
        n = b + 1
        current_length = len(closest_list)
        while(n != b):
            if n == len(self.kBuckets):
                n = 0
            bucket_length = len(self.kBuckets[n].doubles)
            if bucket_length >= kademliaConstants.k_bucket_size - current_length:
                closest_list.extend(self.kBuckets[n].doubles[:kademliaConstants.k_bucket_size - current_length])
                return closest_list

            closest_list.extend(self.kBuckets[n].doubles)
            current_length = current_length + len(self.kBuckets[b].doubles)
            n = n + 1

        return closest_list
            
    def lookup_node(self, key):
        """
        This method will look up nodes that are close to the given key.
        It will return the closest node that it can find.

        key -- The key we are searching for
        """
        def cmp_doubles(d1, d2):
            """
            Compare doubles based on their distance from the key.
            """
            (d1, _) = d1
            (d2, _) = d2
            dist1 = d1 ^ key
            dist2 = d2 ^ key

            if dist1 - dist2 < 0:
                return -1
            elif dist1 - dist2 > 0:
                return 1

            return 0

        # If the key happens to be this node, return ourselves
        if key == self.id:
            return self
        
        # Search for the bucket for this key
        bucket_index = None
        for b in range(len(self.kBuckets)):
            if self.kBuckets[b].in_bucket(key):
                bucket_index = b

        # Get the initial alpha list
        alpha_list = list()
        k_bucket = self.kBuckets[bucket_index]
        if len(k_bucket.doubles) < kademliaConstants.lookup_alpha:
            alpha_list.extend(k_bucket.doubles)

            a_len = len(alpha_list)
            n = bucket_index + 1
            while(n != bucket_index and len(alpha_list) < kademliaConstants.lookup_alpha):
                if n == len(self.kBuckets):

                    n = 0
                alpha_list.extend(self.kBuckets[n].doubles[:kademliaConstants.lookup_alpha - len(alpha_list)])
                n = n + 1

        else:
            alpha_list.extend(k_bucket.doubles[:kademliaConstants.lookup_alpha])

        # If all our k-buckets are completely empty, then stop
        if len(alpha_list) == 0:
            return
        
        # Find the node with the closest ID
        alpha_list.sort(cmp_doubles)
        (_, closest_node) = alpha_list[0]
        old_closest_node = self.id
        k_count = 0

        # Repeatedly find nodes in the system
        while(True):
            klist = list()
            hopDurations = list()

            for (_, a) in alpha_list:
                found_list = a.find_node(key, (self.id, self))
                hopDurations.append(self.rand.random() * kademliaConstants.maximum_RTT_time)
                
                if found_list == None:
                    continue
                
                klist.extend(found_list)

            # Lookups are asynchronous so add in the maximum hopDuration as the time
            # or the timeout time if there was a timeout
            try:
                hopDurations.index(None)
                self.hopDuration = self.hopDuration + kademliaConstants.timeout_time
            except ValueError:
                self.hopDuration = self.hopDuration + max(hopDurations)

            if len(klist) == 0:
                continue
            
            klist.sort(cmp_doubles)
            old_closest_node = closest_node
            (_, c) = klist[0]
            closest_node = c
            
            if closest_node.id == old_closest_node.id or len(klist) >= kademliaConstants.k_bucket_size or k_count == kademliaConstants.k_bucket_size:
                break

            alpha_list = klist[:kademliaConstants.lookup_alpha]

            k_count = k_count + 1
            
        return closest_node
        
    def update_routing_table(self, double):
        """
        Query update the routing table with 

        double -- A 2-tuple of the (ID, node reference) to look up in the routing table
        """
        node_id, node_ref = double
        # Our own information should never be added to the routing table
        if node_id == self.id:
            return
        
        for k in self.kBuckets:
            if k.in_bucket(node_id):
                k.add_node(double)

    def join_network(self, contact_node):
        """
        This method should be called once after a node is created. It
        takes a single contact node and then starts to populate the
        current node's routing table using that contact node.

        contact_node -- A reference to the initial node that this one
        already knows about.
        """
        # Update the routing table with what we already have
        self.update_routing_table((contact_node.id, contact_node))
        contact_node.lookup_node(self.id)
        
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
        string = "\nNode {}, ID hash {}:\n ".format(self.node_name, hex(self.id))
        
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


    def add_node(self, double):
        """
        Add a double comprised of a node ID and a reference to that node to this KBucket.

        double -- A 2-tuple of (node_id, node reference) to add to this KBucket

        WrongKBucketException -- Thrown if the given double's ID is not in this KBucket's space
        """
        node_id, node_ref  = double
        if(not self.in_bucket(node_id)):
            raise WrongKBucketException()
        
        ind = None

        try:
            index = self.doubles.index(double)
            t = self.doubles[index]
            self.doubles.pop(index)
            self.doubles.append(t)
        except ValueError:
            # Not in the k-bucket already
            if(len(self.doubles) < self.k):
                self.doubles.append(double)
                return

            (lrs_id, least_recently_seen_ref) = self.doubles[0]
            if not least_recently_seen_ref.ping((self.node.id, self.node)):
                self.doubles.pop(0)
                self.doubles.append(double)

            # k-bucket is full, throw away this double
                
                
    def in_bucket(self, other_id):
        """
        Determine if a particular ID goes into this kBucket.

        other_id -- The id to check against this KBucket's space
        """
        distance = self.node.id ^ other_id
        if distance >= math.pow(2, self.i) and distance < math.pow(2, self.i + 1):
            return True
        else:
            return False

    def __str__(self):
        """
        Return a string representation of this KBucket including the values of its doubles.
        
        """
        string = "\nkBucket {}: ".format(self.i)

        if(len(self.doubles) == 0):
            return "{}\n\tempty;".format(string)

        for b in self.doubles:
            node_id, node_ref = b
            string = "{}\n\t({}, {});".format(string, node_ref.node_name, hex(node_id) )

        return string

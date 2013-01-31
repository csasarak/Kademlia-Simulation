# Author: Christopher Sasarak
import KademliaConstants

# Implementation of a node object
class Node(object):
    
    def __new__(self, id):
        self.id = ID

        self.kBuckets = list()

        # Populate the Node with empty buckets
        for i in range(0, KademliaConstants.bit_string_size):
            self.kBuckets = KBucket(KademliaConstants.k_bucket_size)

    
    

class KBucket(object):

    def __new__(self, k = None):

        # Use default k size if none is provided
        if(k == None):
            self.k = KConstants.k_bucket_size

        self.bucket_list = list()

# Author: Christopher Sasarak
import KademliaConstants

# Implementation of a node object
class Node(object):
    
    def __new__(self, id):
        self.id = ID

        self.kBuckets = list()

        # Populate the Node with empty buckets
        for i in range(0, KademliaConstants.bit_string_size):
            self.kBuckets = KBucket(self, KademliaConstants.k_bucket_size, i)

    # Return True if a response was received, False otherwise
    def ping(self, triple):
        # passthrough and always answer true for now
        return True

class KBucket(object):

    def __new__(self, i, parent_node, k = None):

        # Use default k size if none is provided
        if(k == None):
            self.k = KConstants.k_bucket_size
        else:
            self.k = k

        self.parent_node = parent_node
        self.bucket_list = list()


    def add_triple(self, triple ):
        if(not self.in_bucket(node_id)):
            return # Should probably return an error value or raise an exception
        
        ip, port, node_id = triple
        ind = None

        try:
            index = self.bucket_list.index(triple)
            t = self.bucket_list[index]
            self.bucket_list.delete(index)
            self.bucket_list.append(t)
        except ValueError:
            # Not in the k-bucket
            if(len(self.bucket_list) < k):
                self.bucket_list.append(triple)
                return

            least_recently_seen = self.bucket_list[0]
            if(not self.parent_node.ping(least_recently_seen)):
                self.bucket_list.delete(0)
                self.bucket_list.append(triple)

            # k-bucket is full, throw away this triple
                
                
    def in_bucket(self, other_id):
        distance = self.parent_node ^ other_id

        if(distance < Math.pow(2, i+1) and distance > Math.pow(2, i)):
            return True
        else:
            return False
    
if(__name__ == "__main__"):
    pass

class OrderedHashtable:
    class Node:
        """This class is used to create nodes in the singly linked "chains" in
        each hashtable bucket."""
        def __init__(self, index, next=None):
            # don't rename the following attributes!
            self.index = index
            self.next = next
        
    def __init__(self, n_buckets=1000):
        # the following two variables should be used to implement the "two-tiered" 
        # ordered hashtable described in class -- don't rename them!
        self.indices = [None] * n_buckets
        self.entries = []
        self.count = 0
        
    def __getitem__(self, key):
        biox=hash(key)%len(self.indices)
        a0=self.indices[biox]
        while a0:
            if a0.index[0]==key:
                return a0.index[1]
            a0=a0.next
            
        else:
            raise KeyError
        
    def __setitem__(self, key, val):
        biox=hash(key)%len(self.indices)
        a0=self.indices[biox]
        while a0:
            if a0.index[0]==key:
                a0.index[1]=val
                return
            a0=a0.next
        else:
            self.indices[biox]=OrderedHashtable.Node(index=[key,val],next=self.indices[biox])
            self.entries.append([key,val])
            self.count+=1
    
    def __delitem__(self, key):
        biox=hash(key)%len(self.indices)
        a0=self.indices[biox]
        if self.indices[biox]==None:
            raise KeyError
        while a0.next:
            if a0.next.index[0]==key:
                self.entries.remove(a0.next.index)
                a0.next=a0.next.next
                self.count-=1   
                return
            a0=a0.next
        if self.indices[biox].index[0]==key:
                self.entries.remove(self.indices[biox].index)
                self.indices[biox]=self.indices[biox].next
                self.count-=1  
                return
        else:
            raise KeyError
            
    def __contains__(self, key):
        try:
            _ = self[key]
            return True
        except:
            return False
        
    def __len__(self):
        return self.count
    
    def __iter__(self): 
        for i in self.entries:
            yield i[0]
                
    def keys(self):
        return iter(self)
    
    def values(self):
        for i in self.entries:
            yield i[1]
            
    def items(self):
        for i in self.entries:
            yield tuple(i)
              
    def __str__(self):
        return '{ ' + ', '.join(str(k) + ': ' + str(v) for k, v in self.items()) + ' }'
            
    def __repr__(self):
        return str(self)
 def rehash(self, size):
        new_buckets = [None] * size
        for i in self.buckets:
            while i is not None:
               print("找到了一次",i.val)
               new_buckets[hash(i.key)%len(new_buckets)]=Hashtable.Node(key=i.key, val=i.val, next=new_buckets[hash(i.key)%len(new_buckets)])
               i=i.next
        
def merge(*lsts):
    merged = []
    # your code here
    Path=Heap()
    a=1
    while a==1:
        a=0
        for i in lsts:
            if len(i)!=0:
                Path.add(i.pop())
                a=1
    while len(Path.data)!=0:
        merged.append(Path.pop_max())
    merged.reverse()
    return merged
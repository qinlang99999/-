class LinkedList:
    class Node:
        def __init__(self, val, prior=None, next=None):
            self.val = val
            self.prior = prior
            self.next  = next
    
    def __init__(self):
        self.head = LinkedList.Node(None) # sentinel node (never to be removed)
        self.head.prior = self.head.next = self.head # set up "circular" topology
        self.length = 0
        self.cursor=None
        
        
    ### prepend and append, below, from class discussion
        
    def prepend(self, value):
        n = LinkedList.Node(value, prior=self.head, next=self.head.next)
        self.head.next.prior = self.head.next = n
        self.length += 1
        
    def append(self, value):
        n = LinkedList.Node(value, prior=self.head.prior, next=self.head)
        n.prior.next = n.next.prior = n
        self.length += 1
            
            
    ### subscript-based access ###
    
    def _normalize_idx(self, idx):
        nidx = idx
        if nidx < 0:
            nidx += len(self)
            if nidx < 0:
                nidx = 0
        return nidx
    
    def __getitem__(self, idx):
        """Implements `x = self[idx]`"""
        n=self.head
        assert(isinstance(idx, int))
        if idx<0:
            idx+=len(self)
        if idx>=len(self) or idx<0:
            raise IndexError
        for i in range(idx+1):
            n=n.next
        return n.val
            
        

    def __setitem__(self, idx, value):
        """Implements `self[idx] = x`"""
        n=self.head
        assert(isinstance(idx, int))
        if idx<0:
            idx+=len(self)
        if idx>=len(self) or idx<0:
            raise IndexError
        for i in range(idx+1):
            n=n.next
        n.val=value
        
    def __delitem__(self, idx):
        """Implements `del self[idx]`"""
        n=self.head
        assert(isinstance(idx, int))
        if idx<0:
            idx+=len(self)
        if idx>=len(self) or idx<0:
            raise IndexError
        
        for i in range(idx+1):
            n=n.next
        n.prior.next=n.next
        n.next.prior=n.prior
        n=n.next
        self.length-=1

    ### cursor-based access ###
    
    def cursor_get(self): 
        """retrieves the value at the current cursor position"""
        assert self.cursor is not self.head
        return self.cursor.val
            


    def cursor_set(self, idx): 
        """sets the cursor to the node at the provided index"""
        assert self.cursor is not self.head
        n=self.head.next
        assert(isinstance(idx, int))
        if idx<0:
            idx+=len(self)
        if idx>=len(self) or idx<0:
            raise IndexError
        for _ in range(idx):
            n=n.next
        self.cursor=n
        


    def cursor_move(self, offset): 
        """moves the cursor forward or backward by the provided offset 
        (a positive or negative integer); note that it is possible to advance 
        the cursor by further than the length of the list, in which case the 
        cursor will just "wrap around" the list, skipping over the sentinel 
        node as needed"""
        assert len(self) > 0
        if offset>=0:
            for _ in range(offset):
                self.cursor=self.cursor.next
                if self.cursor.val==None:
                    self.cursor=self.cursor.next
        elif offset<0:
            for _ in range(-offset):
                self.cursor=self.cursor.prior
                if self.cursor.val==None:
                    self.cursor=self.cursor.prior
        


    def cursor_insert(self, value): 
        """inserts a new value after the cursor and sets the cursor to the 
        new node"""
        assert self.cursor is not self.head
        n= LinkedList.Node(value, prior=self.cursor, next=self.cursor.next)
        self.cursor.next.prior = self.cursor.next = n
        self.cursor=self.cursor.next
        self.length += 1
        
     


    def cursor_delete(self):
        """deletes the node the cursor refers to and sets the cursor to the 
        following node"""
        assert self.cursor is not self.head and len(self) > 0
        self.cursor.prior.next=self.cursor.next
        self.cursor.next.prior=self.cursor.prior
        self.cursor=self.cursor.next
        self.length-=1
        

    ### stringification ###
    
    def __str__(self):
        """Implements `str(self)`. Returns '[]' if the list is empty, else
        returns `str(x)` for all values `x` in this list, separated by commas
        and enclosed by square brackets. E.g., for a list containing values
        1, 2 and 3, returns '[1, 2, 3]'."""
        n=self.head
        AA=[]
        for _ in range(len(self)):
            n=n.next
            AA.append(n.val)
        return str(AA)
        
        
    def __repr__(self):
        """Supports REPL inspection. (Same behavior as `str`.)"""
        return str(self)
        


    ### single-element manipulation ###
        
    def insert(self, idx, value):
        """Inserts value at position idx, shifting the original elements down the
        list, as needed. Note that inserting a value at len(self) --- equivalent
        to appending the value --- is permitted. Raises IndexError if idx is invalid."""
        if idx<len(self):
            n=self.head
            for _ in range(idx+1):
                n=n.next
            af=LinkedList.Node(value, prior=n.prior, next=n)
            n.prior.next = n.prior = af
            self.length +=1
        elif idx==len(self):
            n = LinkedList.Node(value, prior=self.head.prior, next=self.head)
            n.prior.next = n.next.prior = n
            self.length += 1
        else:
            raise IndexError
        
        
    
    def pop(self, idx=-1):
        """Deletes and returns the element at idx (which is the last element,
        by default)."""
        if idx<0:
            idx+=len(self)
        if idx>=len(self) or idx<0:
            raise IndexError
        n=self.head
        for _ in range(idx+1):
            n=n.next
        result=n.val
        n.prior.next=n.next
        n.next.prior=n.prior
        n=n.next
        self.length-=1
        return result
        
    
    def remove(self, value):
        """Removes the first (closest to the front) instance of value from the
        list. Raises a ValueError if value is not found in the list."""
        n=self.head
        for i in range(len(self)):
            n=n.next
            if n.val==value:
                break
            elif i==len(self)-1:
                raise ValueError
        n.prior.next=n.next
        n.next.prior=n.prior
        n=n.next
        self.length-=1
    

    ### predicates (T/F queries) ###
    
    def __eq__(self, other):
        """Returns True if this LinkedList contains the same elements (in order) as
        other. If other is not an LinkedList, returns False."""

        if len(self)==len(other):
            if len(self)==0:
                return True
            else:
                n=self.head
                m=other.head
                for i in range(len(self)):
                    n=n.next
                    m=m.next
                    if n.val!=m.val:
                        return False
                        break
                    if i==len(self)-1:
                        return True
                        break
        else:
            return False
        

    def __contains__(self, value):
        """Implements `val in self`. Returns true if value is found in this list."""
        yyds=0
        n=self.head
        for i in range(len(self)):
            n=n.next
            if n.val==value:
                yyds=1
                break
        if yyds==1:
            return True
        else:
            return False
        


    ### queries ###
    
    def __len__(self):
        """Implements `len(self)`"""
        return self.length
    
    def min(self):
        """Returns the minimum value in this list."""
        n=self.head
        csdn=self.head.next.val
        for _ in range(len(self)):
            n=n.next
            if n.val<csdn:
                csdn=n.val
        return csdn
    
    def max(self):
        """Returns the maximum value in this list."""
        n=self.head
        csdn=self.head.next.val
        for _ in range(len(self)):
            n=n.next
            if n.val>csdn:
                csdn=n.val
        return csdn
        
    
    def index(self, value, i=0, j=None):
        """Returns the index of the first instance of value encountered in
        this list between index i (inclusive) and j (exclusive). If j is not
        specified, search through the end of the list for value. If value
        is not in the list, raise a ValueError."""
        
        if i<0:
            i+=len(self)
        if i>=len(self) or i<0:
            raise ValueError
        if type(j)==int:
            if j<0:
                j+=len(self)
            if j>=len(self) or j<0:
                raise ValueError
        else:
            if j==None:
                j=len(self)
        n=self.head
        result=None
        for _ in range(i):
            n=n.next
        for k in range(i,j):
            n=n.next
            if n.val==value:
                result=k
                break
        if result==None:
            raise ValueError
        else:
            return result
        
    
    def count(self, value):
        """Returns the number of times value appears in this list."""
        csdn=0
        n=self.head
        for _ in range(len(self)):
            n=n.next
            if n.val==value:
                csdn+=1
        return csdn

    
    ### bulk operations ###

    def __add__(self, other):
        """Implements `self + other_list`. Returns a new LinkedList
        instance that contains the values in this list followed by those 
        of other."""
        assert(isinstance(other, LinkedList))
        n=LinkedList()
        k=self.head
        for _ in range(len(self)):
            k=k.next
            m = LinkedList.Node(k.val, prior=n.head.prior, next=n.head)
            m.prior.next = m.next.prior = m
            n.length += 1
        k=other.head
        for _ in range(len(other)):
            k=k.next
            m = LinkedList.Node(k.val, prior=n.head.prior, next=n.head)
            m.prior.next = m.next.prior = m
            n.length += 1
        return n
        
       
    
    def clear(self):
        """Removes all elements from this list."""
        n=LinkedList()
        self.head=n.head
        self.length=n.length
        self.cursor=None
        
        
        
        
    def copy(self):
        """Returns a new LinkedList instance (with separate Nodes), that
        contains the same values as this list."""
        n=LinkedList()
        k=self.head
        for _ in range(len(self)):
            k=k.next
            m = LinkedList.Node(k.val, prior=n.head.prior, next=n.head)
            m.prior.next = m.next.prior = m
            n.length += 1
        return n
        

    def extend(self, other):
        """Adds all elements, in order, from other --- an Iterable --- to this list."""
        """Implements `self + other_list`. Returns a new LinkedList
        instance that contains the values in this list followed by those 
        of other."""
        n=LinkedList()
        k=self.head
        for _ in range(len(self)):
            k=k.next
            m = LinkedList.Node(k.val, prior=n.head.prior, next=n.head)
            m.prior.next = m.next.prior = m
            n.length += 1
        for j in [i for i in other]:
            k=k.next
            m = LinkedList.Node(j, prior=n.head.prior, next=n.head)
            m.prior.next = m.next.prior = m
            n.length += 1
        self.head=n.head
        self.length=n.length
        self.cursor=None
        
        

            
    ### iteration ###

    def __iter__(self):
        """Supports iteration (via `iter(self)`)"""
        n=self.head
        for _ in range(len(self)):
            n=n.next
            yield n.val
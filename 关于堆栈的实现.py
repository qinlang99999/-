delim_openers = '{([<'
delim_closers = '})]>'

def check_delimiters(expr):
    LLL=Stack()
    for i in expr:
        if i!=' ':
            if i in delim_closers and LLL.peek() and LLL.peek() in delim_openers and delim_closers.index(i)==delim_openers.index(LLL.peek()):
                LLL.pop()
            else:
                LLL.push(i)
    return not bool(LLL)
    """Returns True if and only if `expr` contains only correctly matched delimiters, else returns False."""


# you may find the following precedence dictionary useful
prec = {'*': 2, '/': 2,
        '+': 1, '-': 1}

def infix_to_postfix(expr):
    """Returns the postfix form of the infix expression found in `expr`"""
    ops = Stack()
    postfix = []
    toks = expr.split()
    for i in toks:
        if i.isdigit():
            postfix.append(i)
        elif i=='(':
            ops.push(i)
        elif not bool(ops) or ops.peek()=='(':
            ops.push(i)
        elif i==')':
            while ops.peek() and ops.peek()!='(':
                postfix.append(ops.pop())
            if ops.peek()=='(':
                ops.pop()
        elif ops.peek() in list(prec) and prec[ops.peek()]<prec[i]:
            ops.push(i)
        elif ops.peek() in list(prec) and prec[ops.peek()]==prec[i]:
            postfix.append(ops.pop())
            ops.push(i)
        else:
            while ops.peek() in list(prec) and prec[ops.peek()]>prec[i]:
                postfix.append(ops.pop())
                if ops.peek() in list(prec) and prec[ops.peek()]<prec[i]:
                    ops.push(i)
                    break
                elif ops.peek() in list(prec) and prec[ops.peek()]==prec[i]:
                    postfix.append(ops.pop())
                    ops.push(i)
                    break
                elif not ops.peek() or ops.peek() not in list(prec):
                    ops.push(i)
                    break
    while ops.peek():
        postfix.append(ops.pop())
    return ' '.join(postfix)
    
class Queue:
    def __init__(self, limit=10):
        self.data = [None] * limit
        self.head =-1
        self.tail = -1

    def enqueue(self, val):
        if self.head==-1:
            self.head=0
        if self.tail==len(self.data)-1:
            if self.data[0]==None:
                a=[None]*self.head
                b=self.data[self.head:]
                self.data=(b+a)
                self.tail-=self.head
                self.head=-1
            else:
                raise RuntimeError
        self.tail+=1
        self.data[self.tail]=val
        
    def dequeue(self):
        
        if self.head==-1:
            self.head=0
        if self.data[self.head]==None:
            raise RuntimeError      
        a=self.data[self.head]
        self.data[self.head]=None
        self.head+=1
        if self.empty():
            self.head=self.tail=-1
        return a
    
    def resize(self, newsize):
        assert(len(self.data) < newsize)
        if self.head==-1:
            self.head=0
        a=[None]*newsize
        for i in range(self.tail-self.head+1):
            a[i]=self.data[i+self.head]
        self.data=a
        self.tail-=self.head
        self.head=-1
    
    def empty(self):
        a=self.head
        if a==-1:
            a=0
        return a==self.tail+1
    
    def __bool__(self):
        return not self.empty()
    
    def __str__(self):
        if not(self):
            return ''
        return ', '.join(str(x) for x in self)
    
    def __repr__(self):
        return str(self)
    
    def __iter__(self):
        if self.head==-1:
            self.head=0
        a=self.head
        while a!=self.tail+1:
            yield self.data[a]
            a+=1
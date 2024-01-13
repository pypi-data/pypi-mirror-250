import linked_list 
import copy 

class List: 
    def __init__(self): 
        self.innerImpl = linked_list.linked_list() 
    
    def __len__(self): 
        return len(self.innerImpl)

    def __getitem__(self, key): 
        return self.innerImpl[key]

    def __setitem__(self, key, value): 
        self.innerImpl[key] = value
    
    def __delitem__(self, key):
        del self.innerImpl[key] 

    def append(self, value): 
        self.innerImpl.append(value)
       
    def __str__(self): 
        strBuilder = "[" 
        l = len(self) 
        for i in range(l): 
            strBuilder += repr(self[i]) 
            if i != l - 1: 
                strBuilder += ", "
        strBuilder += "]"
        return strBuilder 
    
    def __add__(self, other): 
        self = copy.copy(self) 
        for o in other: 
            self.append(o)
        return self 
    
    def __mul__(self, other): 
        l = len(self) 
        self = copy.copy(self)
        for i in range(other - 1): 
            for j in range(l): 
                self.append(self[j])
        return self 
    
    def __copy__(self): 
        ans = List() 
        for i in self: 
            ans.append(i) 
        return ans
    
    def __eq__(self, other): 
        if type(self) != type(other): 
            return False
        if len(self) != len(other):
            return False
        for i in range(len(self)):
            if self[i] != other[i]: 
                return False 
        return True 

    class Iter: 
        def __init__(self, l): 
            self.l = l 
            self.cur = 0 
            self.end = len(l) 
        
        def __next__(self): 
            if self.cur < self.end: 
                c = self.l[self.cur]
                self.cur += 1
                return c 
            else:
                raise StopIteration 
    
    def __iter__(self): 
        return List.Iter(self)

    def extend(self, other): 
        self += other 
    
    def reverse(self): 
        new = List() 
        for i in reversed(self): 
            new.append(i) 
        del self.innerImpl 
        self.innerImpl = new.innerImpl
    
    def pop(self, i = None): 
        if i is None: 
            i = len(self) - 1
        ans = self[i] 
        del self[i] 
        return ans
    
    def remove(self, x): 
        for i in range(len(self)): 
            if self[i] == x: 
                del self[i] 
                break
        else:
            raise ValueError 
        
    def index(self, x, start = 0, end = None): 
        if end is None: 
            end = len(self) 
        for i in range(start, end): 
            if self[i] == x: 
                return i 
        raise ValueError
    
    def count(self, x): 
        ans = 0 
        for i in self: 
            if i == x: 
                ans += 1
        return ans 

    def insert(self, i, x): 
        self.innerImpl.insert(i, x)

    def sort(self): 
        to_list = [i for i in self]
        to_list.sort() 
        del self.innerImpl
        self.innerImpl = linked_list.linked_list()
        self.extend(to_list)
    
    def copy(self): 
        return copy.copy(self)
    
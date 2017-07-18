# Quelle: https://www.codefellows.org/blog/implementing-a-singly-linked-list-in-python/
class Node(object):
    
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node
    
    def get_data(self):
        return self.data
    
    def get_next(self):
        return self.next_node
    
    def set_next(self, new_next):
        self.next_node = new_next

class UnorderedList(object):
    def __init__(self, head=None):
        self.head = head
    
    def addItem(self, data):
        new_node = Node(data)
        new_node.set_next(self.head)
        self.head = new_node
    
    def size(self):
        current = self.head
        count = 0
        while current:
            count += 1
            current = current.get_next()
        return count
    
    def getItem(self, index):
        count = 0
        r = None
        current = self.head
        if self == None:
            raise Exception("Node is null")
        if index == 0:
            return current.get_data()
        current = current.get_next()
        while current is not None and count <= index:
            count += 1
            if (count == index):
                r = current.get_data()
            current = current.get_next()
        if current is None and r == None:
            raise Exception("index not found")
        return r
    
    def delete(self, data):
        current = self.head
        previous = None
        found = False
        while current and found is False:
            if current.get_data() == data:
                found = True
            else:
                previous = current
                current = current.get_next()
        if current is None:
            raise ValueError("Data not in list")
        if previous is None:
            self.head = current.get_next()
        else:
            previous.set_next(current.get_next())

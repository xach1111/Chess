class Queue:
    class Node:
        def __init__(self, data, next):
            self.data = data
            self.next = next
        
    def __init__(self):
        self.head = None
        self.tail = None
    
    def enqueue(self, data):
        new = Queue.Node(data, None)
        if self.isEmpty():
            self.head = new
        else:
            self.tail.next = new
        self.tail = new
    
    def dequeue(self):
        if not self.isEmpty():
            result = self.head.data
            self.head = self.head.next
            if self.isEmpty():
                self.tail = None
            return result
    def peak(self):
        if not self.isEmpty():
            return self.head.data
        return

    def isEmpty(self):
        return True if self.head == None else False

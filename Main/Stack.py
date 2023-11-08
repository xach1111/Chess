class Stack:
    class Node:
        def __init__(self, data, next):
            self.data = data
            self.next = next

    def __init__(self):
        self.__pointer = None
    
    def push(self, data):    
        self.__pointer = Stack.Node(data, self.__pointer)

    def pop(self):
        if not self.isEmpty():
            result = self.__pointer
            self.__pointer = self.__pointer.next
            return result.data
        return

    def peak(self):
        if not self.isEmpty():
            return self.__pointer.data
        return

    def isEmpty(self):
        return True if self.__pointer == None else False
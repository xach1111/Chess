class Queue:
    def __init__(self, Size):
        self.__queue = [None] * Size
        self.__head = 0
        self.__tail = 0
    
    def Enqueue(self, data):
        if not self.isFull():
            self.__queue[self.__tail] = data
            self.__tail += 1
    
    def Dequeue(self):
        if not self.isEmpty():
            self.__head += 1
            return self.__queue[self.__head - 1]

    def Peak(self):
        if not self.isEmpty():
            return self.__queue[self.__head]

    def isEmpty(self):
        return True if self.__tail == 0 else False

    def isFull(self):
        return True if self.__tail == len(self.__queue) else False
class Stack:
    def __init__(self, Size):
        self.__stack = [None] * Size
        self.__pointer = 0
    
    def push(self, data):
        if not self.isfull():
            self.__stack[self.__pointer] = data
            self.__pointer += 1

    def pop(self):
        if not self.isEmpty():
            self.__pointer -= 1
            return self.__stack[self.__pointer]

    def peak(self):
        if not self.isEmpty():
            return self.__stack[self.__pointer - 1]

    def isEmpty(self):
        return True if self.__pointer == 0 else False
    
    def isfull(self):
        return True if self.__pointer == len(self.__stack) else False
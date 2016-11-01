class Queue:
    def __init__(self):
        self.data = set()

    def isEmpty(self):
        return self.data == {}

    def enqueue(self, item):
        if type(item) == str:
            self.data |= {item}
        else:
            print("Wrong message type to insert")

    def dequeue(self):
        if self.isEmpty():
            print("Queue is Empty")
        else:
            return self.data.pop()

    def size(self):
        return len(self.data)
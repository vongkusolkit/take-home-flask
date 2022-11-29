from model.Node import Node


class LinkedList:
    def __init__(self, values=None):
        self.head = Node(0)
        self.tail = None

    # for human readability when printing (a -> b -> c -> d)
    def __str__(self):
        return ' -> '.join([str(node) for node in self])

    # return number of nodes by iterating over every node until reaching tail
    def __len__(self):
        count = 0
        node = self.head
        while node:
            count += 1
            node = node.next
        return count

    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.next

    # access the values of all nodes
    def values(self):
        return [node.value for node in self]


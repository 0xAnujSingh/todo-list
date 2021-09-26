class TodoItem:
    def __init__(self, msg, done = False):
        self.msg = msg
        self.done = done

    def complete(self):
        self.done = True

    def status(self):
        print(self.done, self.msg)

class TodoList:
    def __init__(self, name):
        self.name = name
        self.items = []

    def add(self, msg):
        item = TodoItem(msg)
        self.items.append(item)
        print("item added")

    def display(self):
        print(self.name)

        index = 0
        for item in self.items:
            print(index, item.done, item.msg)
            index += 1

    def done(self, idx):
        try:
            item = self.items[idx]
            item.complete()
            print("Item marked as Done!")
        except IndexError:
            print("Index not found")

    def undo(self, idx):
        try:
            item = self.items[idx]
            item.done = False
            print("Item marked as Not Done!")
        except IndexError:
            print("Index not found")

    def flush(self):
        self.items.clear()
        print("flush")
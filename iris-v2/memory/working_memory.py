class WorkingMemory:
    def __init__(self, max_items=5):
        self.max_items = max_items
        self.items = []

    def add(self, item):
        self.items.append(item)

        if len(self.items) > self.max_items:
            self.items.pop(0)

    def get_all(self):
        return self.items

    def clear(self):
        self.items = []
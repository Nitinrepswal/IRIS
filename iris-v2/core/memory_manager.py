class MemoryManager:
    def __init__(self, memories=None):
        self.memories = memories or []

    def add(self, memory):
        self.memories.append(memory)

    def update(self, old_memory, new_memory):
        if old_memory in self.memories:
            index = self.memories.index(old_memory)
            self.memories[index] = new_memory
            return True

        return False

    def delete(self, memory):
        if memory in self.memories:
            self.memories.remove(memory)
            return True

        return False

    def find(self, keyword):
        results = []

        for memory in self.memories:
            if keyword.lower() in memory.lower():
                results.append(memory)

        return results

    def get_all(self):
        return self.memories
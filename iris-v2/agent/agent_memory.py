from memory.memory_system import MemorySystem


class AgentMemory:
    def __init__(self):
        self.memory = MemorySystem()

    def remember(self, information):
        self.memory.remember(information)

    def recall(self, query, top_k=3, threshold=0.5):
        return self.memory.recall(
            query,
            top_k=top_k,
            threshold=threshold
        )

    def update(self, old_memory, new_memory):
        return self.memory.update(
            old_memory,
            new_memory
        )

    def forget(self, memory):
        return self.memory.forget(memory)

    def get_all(self):
        return self.memory.get_all()

    def clear(self):
        self.memory.clear()
from memory.long_term_memory import LongTermMemory
from memory.working_memory import WorkingMemory
from models.llm_model import LLMModel
from core.memory_retriever import MemoryRetriever


class MemorySystem:
    def __init__(self):
        self.long_term = LongTermMemory()
        self.working = WorkingMemory()
        self.model = LLMModel()

    def remember(self, memory):
        self.long_term.add(memory)

    def recall(self, query, top_k=3, threshold=0.5):
        memories = self.long_term.get_all()

        if not memories:
            return []

        retriever = MemoryRetriever(
            self.model,
            memories
        )

        return retriever.retrieve(
            query,
            top_k=top_k,
            threshold=threshold
        )

    def update(self, old_memory, new_memory):
        memories = self.long_term.get_all()

        if old_memory not in memories:
            return False

        index = memories.index(old_memory)
        memories[index] = new_memory

        self.long_term.memories = memories
        self.long_term._save()

        return True

    def forget(self, memory):
        memories = self.long_term.get_all()

        if memory not in memories:
            return False

        memories.remove(memory)

        self.long_term.memories = memories
        self.long_term._save()

        return True

    def get_all(self):
        return self.long_term.get_all()

    def clear(self):
        self.long_term.clear()
        self.working.clear()
from memory.long_term_memory import LongTermMemory
from models.llm_model import LLMModel
from core.memory_retriever import MemoryRetriever


class KnowledgeBase:
    def __init__(self):
        self.memory = LongTermMemory()
        self.model = LLMModel()

    def add(self, memory):
        self.memory.add(memory)

    def get_all(self):
        return self.memory.get_all()

    def retrieve(self, query, top_k=3, threshold=0.5):
        memories = self.memory.get_all()

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

    def delete(self, memory):
        memories = self.memory.get_all()

        if memory not in memories:
            return False

        memories.remove(memory)

        self.memory.memories = memories
        self.memory._save()

        return True

    def clear(self):
        self.memory.clear()
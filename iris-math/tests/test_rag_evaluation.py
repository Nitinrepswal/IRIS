import torch
import torch.nn.functional as F


documents = [
    "Python is a high-level programming language.",
    "Machine learning allows computers to learn patterns from data.",
    "Transformers are neural network architectures based on attention.",
    "Vector databases store embeddings and support similarity search."
]


vocabulary = {
    "python": 0,
    "programming": 1,
    "language": 2,
    "machine": 3,
    "learning": 4,
    "computers": 5,
    "patterns": 6,
    "data": 7,
    "transformers": 8,
    "neural": 9,
    "networks": 10,
    "attention": 11,
    "vector": 12,
    "databases": 13,
    "store": 14,
    "embeddings": 15,
    "similarity": 16,
    "search": 17
}


embedding = torch.nn.Embedding(len(vocabulary), 8)


def text_to_vector(text):
    words = (
        text.lower()
        .replace(".", "")
        .replace(",", "")
        .replace("?", "")
        .replace("!", "")
    ).split()

    ids = [
        vocabulary[word]
        for word in words
        if word in vocabulary
    ]

    if not ids:
        return torch.zeros(8)

    ids = torch.tensor(ids, dtype=torch.long)

    return embedding(ids).mean(dim=0)


document_vectors = torch.stack([
    text_to_vector(document)
    for document in documents
])


def retrieve(query, top_k=1):
    query_vector = text_to_vector(query)

    similarities = F.cosine_similarity(
        query_vector.unsqueeze(0),
        document_vectors
    )

    values, indices = torch.topk(similarities, top_k)

    results = []

    for value, index in zip(values, indices):
        results.append({
            "document": documents[index],
            "score": value.item()
        })

    return results


def generate_answer(question):
    question = question.lower()

    if "python" in question:
        return "Python is a high-level programming language."

    if "machine learning" in question:
        return "Machine learning allows computers to learn patterns from data."

    if "transformer" in question:
        return "Transformers are neural network architectures based on attention."

    if "vector database" in question:
        return "Vector databases store embeddings and support similarity search."

    return "I don't know."


test_cases = [
    {
        "question": "What is Python?",
        "expected_document": "Python is a high-level programming language.",
        "expected_answer": "Python is a high-level programming language."
    },
    {
        "question": "What is machine learning?",
        "expected_document": "Machine learning allows computers to learn patterns from data.",
        "expected_answer": "Machine learning allows computers to learn patterns from data."
    },
    {
        "question": "What is a transformer?",
        "expected_document": "Transformers are neural network architectures based on attention.",
        "expected_answer": "Transformers are neural network architectures based on attention."
    },
    {
        "question": "What is a vector database?",
        "expected_document": "Vector databases store embeddings and support similarity search.",
        "expected_answer": "Vector databases store embeddings and support similarity search."
    }
]


retrieval_correct = 0
generation_correct = 0


for test in test_cases:
    question = test["question"]

    results = retrieve(question)

    retrieved_document = results[0]["document"]

    answer = generate_answer(question)

    retrieval_match = retrieved_document == test["expected_document"]
    generation_match = answer == test["expected_answer"]

    if retrieval_match:
        retrieval_correct += 1

    if generation_match:
        generation_correct += 1

    print(f"Question: {question}")
    print(f"Retrieved: {retrieved_document}")
    print(f"Expected document: {test['expected_document']}")
    print(f"Retrieval correct: {retrieval_match}")
    print(f"Generated answer: {answer}")
    print(f"Expected answer: {test['expected_answer']}")
    print(f"Generation correct: {generation_match}")
    print("-" * 50)


retrieval_accuracy = retrieval_correct / len(test_cases)
generation_accuracy = generation_correct / len(test_cases)

print("\nRAG Evaluation Summary:")
print(f"Retrieval accuracy: {retrieval_accuracy:.2f}")
print(f"Generation accuracy: {generation_accuracy:.2f}")
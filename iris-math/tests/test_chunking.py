def chunk_text(text, chunk_size=10, overlap=2):
    words = text.split()

    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size

        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


document = """
Python is a high-level programming language.
It is widely used for artificial intelligence and machine learning.
Machine learning allows computers to learn patterns from data.
Deep learning uses neural networks to learn complex patterns.
Transformers are neural network architectures based on attention.
"""

chunks = chunk_text(
    document,
    chunk_size=10,
    overlap=2
)

print("Original document:")
print(document)

print("\nChunks:")

for i, chunk in enumerate(chunks):
    print(f"Chunk {i + 1}:")
    print(chunk)
    print("-" * 40)
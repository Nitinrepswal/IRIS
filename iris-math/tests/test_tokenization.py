text = "IRIS is an intelligent AI assistant"

tokens = text.split()

vocabulary = {}

for token in tokens:
    if token not in vocabulary:
        vocabulary[token] = len(vocabulary)

print("Tokens:")
print(tokens)

print("\nVocabulary:")
print(vocabulary)

token_ids = [vocabulary[token] for token in tokens]

print("\nToken IDs:")
print(token_ids)

reverse_vocabulary = {index: token for token, index in vocabulary.items()}

decoded_tokens = [reverse_vocabulary[index] for index in token_ids]

print("\nDecoded tokens:")
print(decoded_tokens)

decoded_text = " ".join(decoded_tokens)

print("\nDecoded text:")
print(decoded_text)
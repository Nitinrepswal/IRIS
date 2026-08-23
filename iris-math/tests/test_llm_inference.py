import torch
import torch.nn as nn
import torch.nn.functional as F


torch.manual_seed(42)


text = "iris is an ai assistant"

vocabulary = sorted(set(text))

stoi = {character: index for index, character in enumerate(vocabulary)}
itos = {index: character for character, index in stoi.items()}

encoded_text = torch.tensor(
    [stoi[character] for character in text],
    dtype=torch.long
)


embedding_dimension = 16
num_heads = 2
num_layers = 2


class TinyLanguageModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.embedding = nn.Embedding(
            len(vocabulary),
            embedding_dimension
        )

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embedding_dimension,
            nhead=num_heads,
            batch_first=True
        )

        self.transformer = nn.TransformerEncoder(
            encoder_layer,
            num_layers=num_layers
        )

        self.output_layer = nn.Linear(
            embedding_dimension,
            len(vocabulary)
        )

    def forward(self, token_ids):
        x = self.embedding(token_ids)

        x = self.transformer(x)

        logits = self.output_layer(x)

        return logits


model = TinyLanguageModel()

prompt = "iris"

token_ids = torch.tensor(
    [[stoi[character] for character in prompt]],
    dtype=torch.long
)

print("Prompt:")
print(prompt)

print("\nToken IDs:")
print(token_ids)

with torch.no_grad():
    logits = model(token_ids)

last_logits = logits[:, -1, :]

probabilities = F.softmax(last_logits, dim=-1)

next_token_id = torch.argmax(probabilities, dim=-1).item()

next_character = itos[next_token_id]

print("\nLogits shape:")
print(logits.shape)

print("\nProbability shape:")
print(probabilities.shape)

print("\nNext token:")
print(next_character)

generated_text = prompt + next_character

print("\nGenerated text:")
print(generated_text)
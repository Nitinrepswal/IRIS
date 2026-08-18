import torch
import torch.nn as nn


# --------------------------------------------------
# Input sequence
# --------------------------------------------------

x = torch.tensor([
    [
        [1.0],
        [2.0],
        [3.0],
        [4.0]
    ]
])

print("Input shape:", x.shape)


# --------------------------------------------------
# RNN
# --------------------------------------------------

rnn = nn.RNN(
    input_size=1,
    hidden_size=4,
    batch_first=True
)

rnn_output, rnn_hidden = rnn(x)

print("\nRNN output shape:", rnn_output.shape)
print("RNN hidden shape:", rnn_hidden.shape)

print("\nRNN output:")
print(rnn_output)


# --------------------------------------------------
# LSTM
# --------------------------------------------------

lstm = nn.LSTM(
    input_size=1,
    hidden_size=4,
    batch_first=True
)

lstm_output, (lstm_hidden, lstm_cell) = lstm(x)

print("\nLSTM output shape:", lstm_output.shape)
print("LSTM hidden shape:", lstm_hidden.shape)
print("LSTM cell shape:", lstm_cell.shape)

print("\nLSTM output:")
print(lstm_output)